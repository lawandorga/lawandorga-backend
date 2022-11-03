from typing import Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from core.folders.domain.aggregates.content import Content
from core.folders.domain.external import IOwner
from core.folders.domain.value_objects.encryption import EncryptionPyramid
from core.folders.domain.value_objects.keys import (
    AsymmetricKey,
    FolderKey,
    SymmetricKey,
)
from core.folders.domain.value_objects.keys.base import EncryptedSymmetricKey
from core.seedwork.domain_layer import DomainError


class Folder(IOwner):
    @staticmethod
    def create(name: str = None):
        pk = uuid4()
        return Folder(name=name, pk=pk, keys=[], content={})

    def __init__(
        self,
        name: str = None,
        pk: UUID = None,
        keys: List[FolderKey] = None,
        content: Dict[str, Tuple[Content, EncryptedSymmetricKey]] = None,
        parent: UUID = None,
    ):
        assert name is not None and pk is not None

        self.__pk = pk
        self.__name = name
        self.__content = content if content is not None else {}
        self.__keys = (
            [k if k.is_encrypted else k.encrypt() for k in keys]
            if keys is not None
            else []
        )
        self.__parent = parent

    def __str__(self):
        return "Folder {}".format(self.name)

    @property
    def slug(self):
        return self.__pk

    @property
    def name(self):
        return self.__name

    @property
    def encryption_version(self) -> Optional[str]:
        if len(self.__keys) == 0:
            return None

        versions = []
        for key in self.__keys:
            versions.append(key.key.origin)

        if not all([v == versions[0] for v in versions]):
            raise Exception("Not all folder keys have the same encryption version.")

        return versions[0]

    def __reencrypt_all_keys(self, folder_key: FolderKey):
        # get a new folder key
        a_key = AsymmetricKey.generate()
        new_folder_key = FolderKey(
            key=a_key,
            owner=folder_key.owner,
        )

        # decrypt content keys
        new_content = {}
        for content in self.__content.values():
            enc_content_key = content[1]
            s_key = enc_content_key.decrypt(folder_key.key)
            new_enc_content_key = EncryptedSymmetricKey.create(
                original=s_key, key=new_folder_key.key
            )
            new_content[content[0].name] = (content[0], new_enc_content_key)

        # reencrypt keys
        new_keys = []
        for key in self.__keys:
            new_key = FolderKey(owner=key.owner, key=new_folder_key.key)
            enc_new_key = new_key.encrypt()
            new_keys.append(enc_new_key)

        # set
        self.__content = new_content
        self.__keys = new_keys

    def update_information(self, name=None):
        self.__name = name if name is not None else self.__name

    def __check_encryption_version(self, folder_key: FolderKey):
        encryption_class = EncryptionPyramid.get_highest_asymmetric_encryption()
        if self.encryption_version != encryption_class.VERSION:
            self.__reencrypt_all_keys(folder_key)

    def find_folder_key(self, user: IOwner) -> FolderKey:
        parent_key: Optional[FolderKey] = None

        for key in self.__keys:
            if key.owner.slug == user.slug:
                return key
            if self.__parent and key.owner.slug == self.__parent:
                parent_key = key

        if parent_key is not None:
            return parent_key

        raise DomainError("No folder key was found for this user.")

    def add_content(self, content: Content, key: SymmetricKey, user: IOwner):
        if content.name in self.__content:
            raise DomainError(
                "This folder already contains an item with the same name."
            )
        enc_folder_key = self.find_folder_key(user)
        folder_key = enc_folder_key.decrypt(user)
        enc_key = EncryptedSymmetricKey.create(original=key, key=folder_key.key)
        self.__content[content.name] = (content, enc_key)
        # check
        self.__check_encryption_version(folder_key)

    def update_content(self, content: Content, key: SymmetricKey, user: IOwner):
        if content.name not in self.__content:
            raise DomainError("This folder does not contain an item with this name.")
        enc_folder_key = self.find_folder_key(user)
        folder_key = enc_folder_key.decrypt(user)
        enc_key = EncryptedSymmetricKey.create(original=key, key=folder_key.key)
        self.__content[content.name] = (content, enc_key)
        # check
        self.__check_encryption_version(folder_key)

    def delete_content(self, content: Content):
        if content.name not in self.__content:
            raise DomainError("This folder does not contain an item with this name.")

        del self.__content[content.name]

    def get_key(self) -> "AsymmetricKey":
        if len(self.__keys) == 0:
            raise DomainError("This folder has no keys.")
        return self.__keys[0].key

    def set_parent(self, folder: "Folder", by: IOwner = None):
        self.__parent = folder.slug
        self.grant_access(to=folder, by=by)

    def get_content_key(self, content: Content, user: IOwner):
        if content.name not in self.__content:
            raise DomainError("This folder does not contain the specified item.")

        enc_folder_key = self.find_folder_key(user)
        folder_key = enc_folder_key.decrypt(user)
        enc_key = self.__content[content.name][1]
        content_key = enc_key.decrypt(folder_key.key)
        return content_key

    def get_content_by_name(self, name: str) -> Content:
        if name not in self.__content:
            raise DomainError("This folder does not contain the specified item.")
        return self.__content[name][0]

    def move(self, target: "Folder"):
        pass

    def grant_access(self, to: IOwner, by: Optional[IOwner] = None):

        if len(self.__keys) == 0:
            a_key = AsymmetricKey.generate()

        else:
            assert by is not None
            enc_folder_key = self.find_folder_key(user=by)
            a_key = enc_folder_key.decrypt(by).key

        key = FolderKey(
            owner=to,
            key=a_key,
        )
        enc_key = key.encrypt()
        self.__keys.append(enc_key)
