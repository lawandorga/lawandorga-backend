from django.core.management.base import BaseCommand
from backend.api.models import HasPermission, Group


class Command(BaseCommand):
    def replace_permission(self, delete, replacement):
        for p in HasPermission.objects.filter(permission=delete):
            data = {
                'permission': replacement,
                'user_has_permission': p.user_has_permission,
                'group_has_permission': p.group_has_permission,
                'rlc_has_permission': p.rlc_has_permission
            }
            if not HasPermission.objects.filter(**data):
                HasPermission.objects.create(**data)

    def handle(self, *args, **options):
        for p in HasPermission.objects.exclude(rlc_has_permission=None):
            for g in Group.objects.filter(from_rlc=p.rlc_has_permission):
                HasPermission.objects.create(group_has_permission=g, permission=p.permission)
        # permission_to_delete = Permission.objects.get(name=PERMISSION_MANAGE_GROUP)
        # permission_to_replace = Permission.objects.get(name=PERMISSION_MANAGE_GROUPS_RLC)
        # self.replace_permission(permission_to_delete, permission_to_replace)
        # permission_to_delete.delete()