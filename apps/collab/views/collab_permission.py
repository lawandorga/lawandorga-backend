from apps.collab.serializers import CollabPermissionSerializer
from rest_framework.viewsets import GenericViewSet
from apps.collab.models import CollabPermission
from rest_framework import mixins


class CollabPermissionViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = CollabPermission.objects.all()
    serializer_class = CollabPermissionSerializer