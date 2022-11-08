import abc
from typing import TYPE_CHECKING
from uuid import UUID

from core.folders.domain.types import StrDict
from core.folders.domain.value_objects.keys import SymmetricKey

if TYPE_CHECKING:
    from core.folders.domain.aggregates.folder import Folder


class Item:
    name: str


class Upgrade:
    REPOSITORY: str

    @classmethod
    def create_from_dict(cls, d: StrDict, upgrade: "Upgrade") -> "Upgrade":
        assert (
            "pk" in d
            and isinstance(d["pk"], str)
            and "repository" in d
            and isinstance(d["repository"], str)
        )

        assert d["pk"] == upgrade.pk
        assert d["repository"] == cls.REPOSITORY

        return upgrade

    def __init__(self, folder: "Folder" = None, pk: UUID = None):
        assert folder is not None and pk is not None
        self.__pk = pk
        self.__folder = folder
        self.__folder.add_upgrade(self)

    def __dict__(self) -> StrDict:  # type: ignore
        return {"pk": str(self.__pk), "repository": self.REPOSITORY}

    @property
    def folder(self) -> "Folder":
        return self.__folder

    @property
    def pk(self):
        return self.__pk

    @property
    @abc.abstractmethod
    def content(self) -> list[Item]:
        pass

    @abc.abstractmethod
    def reencrypt(self, old_key: SymmetricKey, new_key: SymmetricKey):
        pass
