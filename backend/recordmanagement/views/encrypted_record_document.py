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
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse
from rest_framework.exceptions import PermissionDenied

from backend.recordmanagement.models.encrypted_record_document import EncryptedRecordDocument
from backend.recordmanagement.models.encrypted_record import EncryptedRecord
from backend.api.models.notification import Notification
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from backend.api.errors import CustomError
from rest_framework import viewsets
from datetime import datetime
import mimetypes
import base64
import pytz
from backend.recordmanagement.serializers import RecordDocumentSerializer, RecordDocumentCreateSerializer
from backend.static.error_codes import ERROR__RECORD__DOCUMENT__ALL_MISSING
from backend.recordmanagement import serializers
from backend.static import error_codes, storage_folders, permissions
from backend.static.encrypted_storage import EncryptedStorage
from backend.static.middleware import get_private_key_from_request
from backend.static.multithreading import MultithreadedFileUploads
from backend.static.storage_management import LocalStorageManager
from backend.static.storage_folders import get_temp_storage_folder


class EncryptedRecordDocumentViewSet(viewsets.ModelViewSet):
    queryset = EncryptedRecordDocument.objects.none()
    serializer_class = RecordDocumentSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RecordDocumentCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return EncryptedRecordDocument.objects.filter(record__from_rlc=self.request.user.rlc)

    def retrieve(self, request: Request, *args, **kwargs):
        if not request.user.has_permission(permissions.PERMISSION_VIEW_RECORDS_RLC):
            raise PermissionDenied()

        instance = self.get_object()

        if not instance.record.user_has_permission(request.user):
            raise PermissionDenied()

        private_key_user = request.user.get_private_key(request=request)
        record_key = instance.record.get_decryption_key(request.user, private_key_user)
        instance.download(record_key)

        file = default_storage.open(instance.get_key())
        response = FileResponse(file, content_type=mimetypes.guess_type(instance.get_file_key())[0])
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(instance.name)
        return response

    def perform_create(self, serializer):
        self.instance = serializer.save()

    def create(self, request, *args, **kwargs):
        if not request.user.has_permission(permissions.PERMISSION_VIEW_RECORDS_RLC):
            raise PermissionDenied()

        response = super().create(request, *args, **kwargs)
        file = request.FILES['file']
        local_file = default_storage.save(self.instance.get_key(), file)
        local_file_path = os.path.join(settings.MEDIA_ROOT, local_file)
        private_key_user = request.user.get_private_key(request=request)
        record_key = self.instance.record.get_decryption_key(request.user, private_key_user)
        EncryptedStorage.encrypt_file_and_upload_to_s3(local_file_path, record_key, self.instance.get_key())
        default_storage.delete(self.instance.get_key())
        default_storage.delete(self.instance.get_file_key())
        return response


class EncryptedRecordDocumentByRecordViewSet(APIView):
    queryset = EncryptedRecordDocument.objects.none()
    serializer_class = RecordDocumentSerializer

    def get(self, request, id):
        """
        downloads all documents from record
        :param request:
        :param id:
        :return:
        """
        if not request.user.has_permission(
            permissions.PERMISSION_VIEW_RECORDS_RLC, for_rlc=request.user.rlc
        ):
            raise CustomError(error_codes.ERROR__API__PERMISSION__INSUFFICIENT)
        try:
            e_record = EncryptedRecord.objects.get(pk=id)
        except Exception as e:
            raise CustomError(error_codes.ERROR__RECORD__RECORD__NOT_EXISTING)

        if not e_record.user_has_permission(request.user):
            raise CustomError(error_codes.ERROR__API__PERMISSION__INSUFFICIENT)

        users_private_key = get_private_key_from_request(request)
        record_key = e_record.get_decryption_key(request.user, users_private_key)
        root_folder_name = (
            storage_folders.get_temp_storage_folder() + "/record" + str(e_record.id)
        )

        for record_document in EncryptedRecordDocument.objects.filter(record=e_record):
            EncryptedStorage.download_from_s3_and_decrypt_file(
                record_document.get_file_key(), record_key, root_folder_name
            )

        # check if all docs are missing?
        if LocalStorageManager.delete_folder_if_empty(root_folder_name):
            LocalStorageManager.delete_folder_if_empty(
                storage_folders.get_temp_storage_folder()
            )
            raise CustomError(ERROR__RECORD__DOCUMENT__ALL_MISSING)

        LocalStorageManager.zip_folder_and_delete(root_folder_name, root_folder_name)
        return LocalStorageManager.create_response_from_zip_file(
            root_folder_name + ".zip"
        )

    def post(self, request, id):


        try:
            e_record: EncryptedRecord = EncryptedRecord.objects.get(pk=id)
        except Exception as e:
            raise CustomError(error_codes.ERROR__RECORD__RECORD__NOT_EXISTING)

        if not e_record.user_has_permission(request.user):
            raise CustomError(error_codes.ERROR__API__PERMISSION__INSUFFICIENT)

        users_private_key: bytes = get_private_key_from_request(request)

        files = request.FILES.getlist("files")
        if files.__len__() == 0:
            raise CustomError(error_codes.ERROR__FILES__NO_FILES_TO_UPLOAD)
        local_file_information = LocalStorageManager.save_files_locally(files)
        filepaths: [str] = [n["local_file_path"] for n in local_file_information]

        directory: str = storage_folders.get_storage_folder_encrypted_record_document(
            e_record.from_rlc_id, e_record.id
        )
        record_key: str = e_record.get_decryption_key(request.user, users_private_key)
        MultithreadedFileUploads.encrypt_files_and_upload_to_single_s3_folder(
            filepaths, directory, record_key
        )

        e_record_documents_handled = []
        for file_information in local_file_information:
            already_existing: EncryptedRecordDocument = EncryptedRecordDocument.objects.filter(
                record=e_record, name=file_information["file_name"]
            ).first()
            if already_existing is not None:
                already_existing.file_size = file_information["file_size"]
                already_existing.last_edited = datetime.now().replace(tzinfo=pytz.utc)
                already_existing.creator = request.user
                already_existing.save()
                e_record_documents_handled.append(already_existing)

                Notification.objects.notify_record_document_modified(
                    request.user, already_existing
                )
            else:
                new_encrypted_record_document = EncryptedRecordDocument(
                    record=e_record,
                    creator=request.user,
                    file_size=file_information["file_size"],
                    name=file_information["file_name"],
                )
                new_encrypted_record_document.save()

                Notification.objects.notify_record_document_added(
                    request.user, new_encrypted_record_document
                )
                e_record_documents_handled.append(new_encrypted_record_document)
        return Response(
            serializers.OldEncryptedRecordDocumentSerializer(
                e_record_documents_handled, many=True
            ).data
        )


class EncryptedRecordDocumentDownloadViewSet(APIView):
    def get(self, request: Request, id: str):
        """
        download single document from file
        :param request:
        :param id:
        :return:
        """
        try:
            e_record_document = EncryptedRecordDocument.objects.get(pk=id)
        except:
            raise CustomError(error_codes.ERROR__RECORD__DOCUMENT__NOT_FOUND)
        e_record = e_record_document.record

        if not e_record.user_has_permission(request.user):
            raise CustomError(error_codes.ERROR__API__PERMISSION__INSUFFICIENT)
        users_private_key = get_private_key_from_request(request)
        record_key = e_record.get_decryption_key(request.user, users_private_key)

        EncryptedStorage.download_from_s3_and_decrypt_file(
            e_record_document.get_file_key(),
            record_key,
            storage_folders.get_temp_storage_folder(),
        )

        local_file_path = storage_folders.get_temp_storage_path(e_record_document.name)
        file = base64.b64encode(open(local_file_path, "rb").read())
        res = Response(file, content_type=mimetypes.guess_type(e_record_document.name))
        res["Content-Disposition"] = (
            'attachment; filename="' + e_record_document.name + '"'
        )
        LocalStorageManager.delete_file(local_file_path)
        LocalStorageManager.delete_folder_if_empty(get_temp_storage_folder())
        return res
