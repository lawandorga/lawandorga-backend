from typing import cast

from django.db import transaction

from core.auth.models import RlcUser
from core.data_sheets.models import DataSheet
from core.folders.api import schemas
from core.folders.domain.repositories.item import ItemRepository
from core.folders.domain.value_objects.tree import TreeAccess
from core.folders.use_cases.folder import get_repository
from core.seedwork.api_layer import Router
from core.seedwork.repository import RepositoryWarehouse

router = Router()


@router.get(output_schema=schemas.OutputFolderPage)
def query__list_folders(rlc_user: RlcUser):
    r = get_repository()
    tree = r.tree(rlc_user, rlc_user.org_id)

    available_persons = RlcUser.objects.filter(org_id=rlc_user.org_id)

    return {"tree": tree.as_dict(), "available_persons": list(available_persons)}


@router.get(url="available_folders/", output_schema=list[schemas.OutputAvailableFolder])
def query__available_folders(rlc_user: RlcUser):
    r = get_repository()
    folders_1 = r.get_list(rlc_user.org_id)
    folders_2 = list(map(lambda f: {"id": f.uuid, "name": f.name}, folders_1))
    return folders_2


@router.get(
    url="<uuid:id>/",
    output_schema=schemas.OutputFolderDetail,
)
def query__detail_folder(rlc_user: RlcUser, data: schemas.InputFolderDetail):
    r = get_repository()
    folder = r.retrieve(rlc_user.org_id, data.id)
    folders_dict = r.get_dict(rlc_user.org_id)
    users = list(RlcUser.objects.filter(org_id=rlc_user.org_id))
    users_dict = {u.uuid: u for u in users}
    access = TreeAccess(folders_dict, folder, users_dict)

    for item in folder.items:
        if item.repository == "RECORD":
            item_repository = cast(
                ItemRepository, RepositoryWarehouse.get(item.repository)
            )
            record = cast(DataSheet, item_repository.retrieve(item.uuid, folder.org_pk))
            with transaction.atomic():
                for file in list(record.documents.all()):
                    if file.key is None and file.record:
                        file.key = file.record.key
                        file.save()
                    if file.folder_uuid is None:
                        file.folder_uuid = folder.uuid
                        folder.add_item(file)
                        file.save()
                r.save(folder)

    subfolders = r.get_children(rlc_user.org_id, folder.uuid)

    return {
        "folder": folder.as_dict(),
        "content": folder.items,
        "subfolders": subfolders,
        "access": access.as_dict(),
    }
