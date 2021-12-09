#  law&orga - record and organization management software for refugee law clinics
#  Copyright (C) 2019  Dominik Walser
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
from apps.api.serializers import RlcNameSerializer, RlcSerializer
from apps.api.models.rlc import Rlc
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework import mixins


class RlcViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Rlc.objects.all()
    serializer_class = RlcSerializer

    def get_queryset(self) -> QuerySet:
        queryset = Rlc.objects.all().order_by("name")
        return queryset

    def get_authenticators(self):
        # self.action == 'list' would be better here but self.action is not set yet
        if self.request.path == "/api/rlcs/" and self.request.method == "GET":
            return []
        return super().get_authenticators()

    def get_permissions(self):
        if self.action == 'list':
            return []
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return RlcNameSerializer
        return super().get_serializer_class()