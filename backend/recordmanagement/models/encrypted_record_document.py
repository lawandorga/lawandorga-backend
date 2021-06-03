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

from backend.static.encrypted_storage import EncryptedStorage
from backend.static.encryption import AESEncryption
from backend.static.storage_folders import get_storage_folder_encrypted_record_document
from django.db.models.signals import pre_delete
from backend.api.models import UserProfile, EncryptedModelMixin
from django.dispatch import receiver
from django.db import models


class EncryptedRecordDocument(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(
        UserProfile,
        related_name="e_record_documents_created",
        on_delete=models.SET_NULL,
        null=True,
    )

    record = models.ForeignKey(
        "EncryptedRecord", related_name="e_record_documents", on_delete=models.CASCADE
    )

    created_on = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now_add=True)

    file_size = models.BigIntegerField(null=True)

    tagged = models.ManyToManyField(
        "RecordDocumentTag", related_name="e_tagged", blank=True
    )

    class Meta:
        verbose_name = "RecordDocument"
        verbose_name_plural = "RecordDocuments"

    def __str__(self):
        return "recordDocument: {}; name: {}; creator: {}; record: {};".format(
            self.pk, self.name, self.creator.email, self.record.record_token
        )

    def get_key(self):
        return '{}{}'.format(
            get_storage_folder_encrypted_record_document(self.record.from_rlc.pk, self.record.id),
            self.name
        )

    def get_file_key(self):
        return '{}.enc'.format(self.get_key())

    def get_folder(self):
        return get_storage_folder_encrypted_record_document(
            self.record.from_rlc.pk, self.record.id
        )

    def download(self, record_key):
        key = self.get_file_key()
        downloaded_file_path = os.path.join(settings.MEDIA_ROOT, key)
        folder_path = downloaded_file_path[:downloaded_file_path.rindex('/')]
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        EncryptedStorage.get_s3_client().download_file(settings.SCW_S3_BUCKET_NAME, key, downloaded_file_path)
        AESEncryption.decrypt_file(downloaded_file_path, record_key)

    def delete_on_cloud(self):
        try:
            EncryptedStorage.delete_on_s3(self.get_file_key())
        except:
            print("couldnt delete " + self.name + " on cloud")

    @receiver(pre_delete)
    def pre_deletion(sender, instance, **kwargs):
        if sender == EncryptedRecordDocument:
            instance.delete_on_cloud()
