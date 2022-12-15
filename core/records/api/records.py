from typing import cast

from core.auth.models import RlcUser
from core.folders.domain.repositiories.folder import FolderRepository
from core.records.api import schemas
from core.records.use_cases.access_delivery import optimize__deliver_access
from core.records.use_cases.record import create_a_record_and_a_folder
from core.seedwork.api_layer import Router
from core.seedwork.repository import RepositoryWarehouse

router = Router()


@router.post(
    input_schema=schemas.InputRecordCreate, output_schema=schemas.OutputRecordCreate
)
def command__create_record(rlc_user: RlcUser, data: schemas.InputRecordCreate):
    folder_repository = cast(
        FolderRepository, RepositoryWarehouse.get(FolderRepository)
    )
    folder = folder_repository.get_or_create_records_folder(rlc_user.org_id, rlc_user)
    record_pk = create_a_record_and_a_folder(
        rlc_user, data.name, parent_folder=folder.uuid, template=data.template
    )
    return {"id": record_pk}


@router.post(url="optimize/")
def command__deliver_access(rlc_user: RlcUser):
    optimize__deliver_access(rlc_user)
