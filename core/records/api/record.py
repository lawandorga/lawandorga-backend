from core.auth.models.org_user import RlcUser
from core.data_sheets.use_cases.record import create_a_data_sheet_within_a_folder
from core.records.use_cases.record import change_record_token, create_record
from core.seedwork.api_layer import Router

from . import schemas

router = Router()


@router.post(output_schema=schemas.OutputCreateRecord)
def command__create_record(rlc_user: RlcUser, data: schemas.InputCreateRecord):
    folder_uuid = create_record(rlc_user, data.token)
    if data.template:
        create_a_data_sheet_within_a_folder(
            rlc_user, data.token, folder_uuid, data.template
        )
    return {"folder_uuid": folder_uuid}


@router.put(url="<uuid:uuid>/change_token/")
def command__change_record_token(
    rlc_user: RlcUser, data: schemas.InputChangeRecordToken
):
    change_record_token(rlc_user, data.uuid, data.token)