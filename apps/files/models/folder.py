from apps.files.static import PERMISSION_READ_FOLDER, PERMISSION_WRITE_FOLDER
from apps.files.models.folder_permission import FolderPermission
from apps.static.storage_folders import get_storage_base_files_folder
from apps.api.static import PERMISSION_MANAGE_FOLDER_PERMISSIONS_RLC, PERMISSION_READ_ALL_FOLDERS_RLC, \
    PERMISSION_WRITE_ALL_FOLDERS_RLC
from apps.api.models.rlc import Rlc
from apps.api.models import UserProfile
from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", related_name="child_folders", null=True, on_delete=models.CASCADE, blank=True)
    rlc = models.ForeignKey(Rlc, related_name="folders", on_delete=models.CASCADE, null=False, blank=True)

    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"

    def __str__(self) -> str:
        return "folder: {}; name: {};".format(self.pk, self.name)

    def get_file_key(self) -> str:
        if self.parent:
            key = self.parent.get_file_key()
        else:
            key = get_storage_base_files_folder(self.rlc.id)
        return key + self.name + "/"

    def get_all_parents(self):
        if not self.parent:
            return []
        elif self.parent.parent:
            return self.parent.get_all_parents() + [self.parent]
        else:
            return [self.parent]

    def get_all_children(self):
        if not self.child_folders:
            return []
        children = []
        for child in self.child_folders.all():
            children.append(child)
            children += child.get_all_children()
        return children

    def user_has_permission_read(self, user: UserProfile) -> bool:
        from apps.files.models.permission_for_folder import PermissionForFolder

        if user.rlc != self.rlc:
            return False

        if (
            user.has_permission(PERMISSION_READ_ALL_FOLDERS_RLC)
            or user.has_permission(PERMISSION_WRITE_ALL_FOLDERS_RLC)
            or user.has_permission(PERMISSION_MANAGE_FOLDER_PERMISSIONS_RLC)
        ):
            return True

        relevant_folders = self.get_all_parents() + [self]
        users_groups = user.rlcgroups.all()
        p_read = FolderPermission.objects.get(name=PERMISSION_READ_FOLDER)
        if PermissionForFolder.objects.filter(
            folder__in=relevant_folders,
            group_has_permission__in=users_groups,
            permission=p_read,
        ).exists():
            return True

        return False

    def user_has_permission_write(self, user: UserProfile) -> bool:
        from apps.files.models.permission_for_folder import PermissionForFolder

        if user.rlc != self.rlc:
            return False

        if (
            user.has_permission(PERMISSION_WRITE_ALL_FOLDERS_RLC) or
            user.has_permission(PERMISSION_MANAGE_FOLDER_PERMISSIONS_RLC)
        ):
            return True

        relevant_folders = self.get_all_parents() + [self]
        users_groups = user.rlcgroups.all()
        p_write = FolderPermission.objects.get(name=PERMISSION_WRITE_FOLDER)

        relevant_permissions = PermissionForFolder.objects.filter(
            folder__in=relevant_folders,
            group_has_permission__in=users_groups,
            permission=p_write,
        )
        if relevant_permissions.count() >= 1:
            return True

        return False

    def user_can_see_folder(self, user: UserProfile) -> bool:
        from apps.files.models.permission_for_folder import PermissionForFolder

        if (
            user.has_permission(PERMISSION_WRITE_ALL_FOLDERS_RLC) or
            user.has_permission(PERMISSION_MANAGE_FOLDER_PERMISSIONS_RLC)
        ):
            return True

        folders = self.get_all_parents() + [self] + self.get_all_children()
        users_groups = user.rlcgroups.all()
        if PermissionForFolder.objects.filter(folder__in=folders, group_has_permission__in=users_groups).exists():
            return True
        return False
