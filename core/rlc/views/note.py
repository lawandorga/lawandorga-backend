from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from core.models import Note
from core.seedwork.permission import CheckPermissionWall
from core.static import PERMISSION_DASHBOARD_MANAGE_NOTES

from ..serializers import NoteSerializer


class NoteViewSet(
    CheckPermissionWall,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = NoteSerializer
    permission_wall = {
        "create": PERMISSION_DASHBOARD_MANAGE_NOTES,
        "update": PERMISSION_DASHBOARD_MANAGE_NOTES,
        "partial_update": PERMISSION_DASHBOARD_MANAGE_NOTES,
        "destroy": PERMISSION_DASHBOARD_MANAGE_NOTES,
    }
    queryset = Note.objects.none()

    def get_queryset(self):
        return Note.objects.filter(rlc=self.request.user.rlc)