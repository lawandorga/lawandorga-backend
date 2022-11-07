from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from core.auth.models import RlcUser
import uuid


def get_ics_calendar(request, calendar_uuid: uuid):
    user = get_object_or_404(RlcUser, calendar_uuid=calendar_uuid)
    calendar = user.get_ics_calendar()
    return HttpResponse(calendar, content_type="text/calendar")
