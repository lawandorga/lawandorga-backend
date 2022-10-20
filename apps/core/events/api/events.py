from typing import List

from django.core.exceptions import ObjectDoesNotExist

from apps.core.auth.models import RlcUser
from apps.core.events.api.schemas import (
    InputEventCreate,
    InputEventDelete,
    InputEventUpdate,
    OutputEventResponse,
)
from apps.core.events.models import Event
from apps.core.rlc.models import Org
from apps.static.api_layer import ApiError, Router

router = Router()


@router.api(output_schema=List[OutputEventResponse])
def get_all_events_for_user(rlc_user: RlcUser):
    events: List[OutputEventResponse] = Event.get_all_events_for_user(rlc_user)
    return events


@router.api(
    method="POST",
    input_schema=InputEventCreate,
    output_schema=OutputEventResponse,
    auth=True,
)
def create_event(data: InputEventCreate, rlc_user: RlcUser):
    org_list = Org.objects.filter(id=rlc_user.org.id)
    event = org_list[0].events.create(
        is_global=data.is_global,
        name=data.name,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
    )
    return event


@router.api(
    url="<int:id>/",
    method="PUT",
    input_schema=InputEventUpdate,
    output_schema=OutputEventResponse,
    auth=True,
)
def update_event(data: InputEventUpdate, rlc_user: RlcUser):
    try:
        event = Event.objects.get(id=data.id)
    except ObjectDoesNotExist:
        raise ApiError("The event you want to edit does not exist.")

    if rlc_user.org.id != event.org.id:
        raise ApiError(
            "You do not have the permission to edit this event.",
        )

    event.update_information(data)

    return event


@router.api(url="<int:id>/", method="DELETE", input_schema=InputEventDelete)
def delete_event(data: InputEventDelete, rlc_user: RlcUser):
    try:
        event = Event.objects.get(id=data.id)
    except ObjectDoesNotExist:
        raise ApiError("The event you want to delete does not exist.")
    if rlc_user.org.id != event.org.id:
        raise ApiError(
            "You do not have the permission to delete this event.",
        )

    event.delete()
