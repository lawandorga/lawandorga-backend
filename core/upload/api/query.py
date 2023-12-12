import mimetypes

from django.contrib.auth.models import AnonymousUser
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from core.auth.models import OrgUser
from core.seedwork.api_layer import Router

from ..models import UploadLink
from . import schemas

router = Router()


@router.get(
    url="<uuid:uuid>/",
    output_schema=schemas.OutputQueryLink,
)
def query__link(rlc_user: OrgUser, data: schemas.InputQueryLink):
    link = get_object_or_404(UploadLink, org_id=rlc_user.org_id, uuid=data.uuid)
    return {
        "uuid": link.uuid,
        "name": link.name,
        "link": link.link,
        "created": link.created,
        "disabled": link.disabled,
        "files": list(link.files.all()),
    }


@router.get(
    url="<uuid:uuid>/public/",
    output_schema=schemas.OutputQueryLinkPublic,
)
def query__link_public(anonymous_user: AnonymousUser, data: schemas.InputQueryLink):
    link = get_object_or_404(UploadLink, uuid=data.uuid)
    return link


@router.get(
    url="<uuid:link>/<uuid:file>/",
    output_schema=FileResponse,
)
def query__download_file(rlc_user: OrgUser, data: schemas.InputDownloadFile):
    link = get_object_or_404(UploadLink, org_id=rlc_user.org_id, uuid=data.link)

    filename, file = link.download(data.file, rlc_user)

    response = FileResponse(
        file, filename=filename, content_type=mimetypes.guess_type(filename)[0]
    )
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
    return response
