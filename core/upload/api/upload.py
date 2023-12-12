from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import UploadedFile

from core.auth.models import OrgUser
from core.seedwork.api_layer import ApiError, Router
from core.upload.use_cases.upload import (
    create_upload_link,
    delete_upload_link,
    disable_upload_link,
    upload_data,
)

from . import schemas

router = Router()


@router.post(url="")
def command__create_link(rlc_user: OrgUser, data: schemas.InputCreateLink):
    create_upload_link(rlc_user, data.name, data.folder)


@router.post(url="<uuid:link>/disable/")
def command__disable_link(rlc_user: OrgUser, data: schemas.InputDisableLink):
    disable_upload_link(rlc_user, data.link)


@router.post(url="<uuid:link>/upload/")
def command__upload_file(anonymous_user: AnonymousUser, data: schemas.InputUploadFile):
    if not isinstance(data.file, UploadedFile):
        raise ApiError({"file": ["You need to submit a file"]})

    upload_data(anonymous_user, data.name, data.file, data.link)


@router.delete(url="<uuid:link>/")
def command__delete_link(rlc_user: OrgUser, data: schemas.InputDeleteLink):
    delete_upload_link(rlc_user, data.link)
