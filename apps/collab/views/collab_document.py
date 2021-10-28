#  law&orga - record and organization management software for refugee law clinics
#  Copyright (C) 2020  Dominik Walser
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>

from typing import Any
from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from apps.api.errors import CustomError
from apps.api.models import Group, HasPermission, Permission
from apps.api.serializers import OldHasPermissionSerializer
from apps.collab.models import (
    CollabDocument,
    CollabPermission,
    PermissionForCollabDocument,
)
from apps.collab.serializers import (
    CollabDocumentSerializer,
    CollabDocumentTreeSerializer,
    PermissionForCollabDocumentNestedSerializer,
    PermissionForCollabDocumentSerializer, TextDocumentVersionSerializer, CollabDocumentCreateSerializer,
    CollabDocumentListSerializer,
)
from apps.static.error_codes import ERROR__API__PERMISSION__INSUFFICIENT
from apps.static.permissions import (
    PERMISSION_MANAGE_COLLAB_DOCUMENT_PERMISSIONS_RLC,
    PERMISSION_READ_ALL_COLLAB_DOCUMENTS_RLC,
    PERMISSION_WRITE_ALL_COLLAB_DOCUMENTS_RLC,
)


class CollabDocumentViewSet(viewsets.ModelViewSet):
    queryset = CollabDocument.objects.none()
    serializer_class = CollabDocumentSerializer

    def get_serializer_class(self):
        if self.action in ['create']:
            return CollabDocumentCreateSerializer
        elif self.action in ['list']:
            return CollabDocumentListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = CollabDocument.objects.filter(rlc=self.request.user.rlc)
        if (
            self.request.user.has_permission(PERMISSION_READ_ALL_COLLAB_DOCUMENTS_RLC)
            or self.request.user.has_permission(PERMISSION_WRITE_ALL_COLLAB_DOCUMENTS_RLC)
            or self.request.user.has_permission(PERMISSION_MANAGE_COLLAB_DOCUMENT_PERMISSIONS_RLC)
        ):
            return queryset
        else:
            queryset = list(queryset)
            permissions = list(self.request.user.get_collab_permissions())

            def access(doc):
                for permission in permissions:
                    permission_path = permission.document.path
                    if doc.path.startswith(permission_path):
                        return True
                return False

            return [doc for doc in queryset if access(doc)]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def list(self, request: Request, **kwargs: Any) -> Response:
    #     user_has_overall_permission: bool = (
    #         request.user.has_permission(PERMISSION_READ_ALL_COLLAB_DOCUMENTS_RLC)
    #         or request.user.has_permission(PERMISSION_WRITE_ALL_COLLAB_DOCUMENTS_RLC)
    #         or request.user.has_permission(PERMISSION_MANAGE_COLLAB_DOCUMENT_PERMISSIONS_RLC)
    #     )
    #     if user_has_overall_permission:
    #         queryset = self.get_queryset().exclude(path__contains="/").order_by("path")
    #         data = CollabDocumentTreeSerializer(
    #             instance=queryset,
    #             user=request.user,
    #             all_documents=self.get_queryset().order_by("path"),
    #             overall_permission=user_has_overall_permission,
    #             see_subfolders=False,
    #             many=True,
    #             context={request: request},
    #         ).data
    #     else:
    #         queryset = self.get_queryset().exclude(path__contains="/").order_by("path")
    #         data = []
    #         for document in queryset:
    #             see, direct = document.user_can_see(request.user)
    #             if see:
    #                 data.append(
    #                     CollabDocumentTreeSerializer(
    #                         instance=document,
    #                         user=request.user,
    #                         all_documents=self.get_queryset().order_by("path"),
    #                         overall_permission=user_has_overall_permission,
    #                         many=False,
    #                         see_subfolders=direct,
    #                         context={request: request},
    #                     ).data
    #                 )
    #     return Response(data)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if not CollabDocument.user_has_permission_write(
            self.get_object().path, request.user
        ):
            raise CustomError(ERROR__API__PERMISSION__INSUFFICIENT)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def latest(self, request, *args, **kwargs):
        instance = self.get_object()
        versions = instance.versions.all()
        latest_version = versions.order_by('-created').first()
        if latest_version is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        latest_version.decrypt(
            request.user.rlc.get_aes_key(user=request.user,
                                         private_key_user=request.user.get_private_key(request=request)))
        return Response(TextDocumentVersionSerializer(latest_version).data)

    @action(detail=True, methods=["get", "post"])
    def permissions(self, request: Request, pk: int):
        document = self.get_object()

        if not request.user.has_permission(
            PERMISSION_MANAGE_COLLAB_DOCUMENT_PERMISSIONS_RLC, for_rlc=request.user.rlc
        ):
            raise CustomError(ERROR__API__PERMISSION__INSUFFICIENT)

        if request.method == "GET":

            permissions_direct = PermissionForCollabDocument.objects.filter(
                document__path=document.path
            )
            permissions_below = PermissionForCollabDocument.objects.filter(
                document__path__startswith="{}/".format(document.path),
            ).exclude(document__path=document.path)

            permissions_above = []
            parts = document.path.split("/")
            i = 0
            while True:
                current_path = ""
                for j in range(i + 1):
                    if current_path != "":
                        current_path += "/"
                    current_path += parts[j]
                as_list = list(
                    PermissionForCollabDocument.objects.filter(
                        document__path=current_path
                    ).exclude(document__path=document.path)
                )
                permissions_above += as_list
                i += 1
                if i >= parts.__len__() - 1:
                    break

            overall_permissions_strings = [
                PERMISSION_MANAGE_COLLAB_DOCUMENT_PERMISSIONS_RLC,
                PERMISSION_WRITE_ALL_COLLAB_DOCUMENTS_RLC,
                PERMISSION_READ_ALL_COLLAB_DOCUMENTS_RLC,
            ]
            overall_permissions = Permission.objects.filter(
                name__in=overall_permissions_strings
            )
            has_permissions_for_groups = HasPermission.objects.filter(
                permission__in=overall_permissions,
            )

            return_object = {
                "from_above": PermissionForCollabDocumentNestedSerializer(
                    permissions_above, many=True
                ).data,
                "from_below": PermissionForCollabDocumentNestedSerializer(
                    permissions_below, many=True
                ).data,
                "direct": PermissionForCollabDocumentNestedSerializer(
                    permissions_direct, many=True
                ).data,
                "general": OldHasPermissionSerializer(
                    has_permissions_for_groups, many=True
                ).data,
            }
            return Response(return_object)
        if request.method == "POST":
            try:
                permission_for_document = PermissionForCollabDocument.objects.create(
                    group_has_permission_id=request.data["group_id"],
                    permission_id=request.data["permission_id"],
                    document=document,
                )
            except Exception as e:
                raise CustomError("invalid arguments")

            return Response(
                PermissionForCollabDocumentSerializer(permission_for_document).data,
                status=201,
            )
