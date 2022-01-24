from apps.static.storage_folders import clean_filename
from django.core.files.storage import default_storage
from apps.static.encryption import AESEncryption
from apps.api.models.user import UserProfile
from apps.static.storage import download_and_decrypt_file, encrypt_and_upload_file
from django.core.files import File as DjangoFile
from django.utils import timezone
from django.db import models
from .folder import Folder
import unicodedata
import re


class File(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(UserProfile, related_name="files_created", on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey(Folder, related_name="files_in_folder", on_delete=models.CASCADE)
    key = models.CharField(null=True, max_length=1000, unique=True)
    file = models.FileField(upload_to='files/file/', blank=True, null=True)
    exists = models.BooleanField(default=True)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ['exists', '-created']

    def __str__(self):
        return "file: {}; fileKey: {};".format(self.pk, self.get_file_key())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.key = self.slugify()
        if not self.exists:
            self.exists = default_storage.exists(self.get_encrypted_file_key())
        super().save(*args, **kwargs)
        for parent in self.get_parents():
            parent.last_edited = timezone.now()
            parent.save()

    def delete(self, *args, **kwargs):
        self.delete_on_cloud()
        super().delete(*args, **kwargs)

    def get_parents(self):
        return self.folder.get_all_parents() + [self.folder]

    def slugify(self, unique=None):
        key = '{}{}'.format(self.folder.get_file_key(), self.name)
        if unique is not None:
            key = '{}{}_{}'.format(self.folder.get_file_key(), unique, self.name)
        special_char_map = {ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('ß'): 'ss', ord('Ä'): 'AE',
                            ord('Ö'): 'OE', ord('Ü'): 'UE'}
        key = key.translate(special_char_map)
        unicodedata.normalize('NFKC', key).encode('ascii', 'ignore').decode('ascii')
        key = re.sub(r'[^/.\w\s-]', '', key.lower()).strip()
        key = re.sub(r'[-\s]+', '-', key)
        if not File.objects.filter(key=key).exists():
            return key
        else:
            unique = 1 if unique is None else unique + 1
            return self.slugify(unique=unique)

    def get_file_key(self):
        return self.key

    def generate_key(self):
        if self.key is None:
            key = self.folder.get_file_key() + clean_filename(self.name)
            self.key = key
            self.save()

    def get_encrypted_file_key(self):
        return self.get_file_key() + ".enc"

    @staticmethod
    def encrypt_file(file, aes_key_rlc=None):
        if aes_key_rlc:
            key = aes_key_rlc
        else:
            raise ValueError("You need to pass (aes_key_rlc).")
        name = file.name
        file = AESEncryption.encrypt_in_memory_file(file, key)
        file = DjangoFile(file, name='{}.enc'.format(name))
        return file

    def decrypt_file(self, aes_key_rlc=None):
        if aes_key_rlc:
            key = aes_key_rlc
        else:
            raise ValueError("You need to pass (aes_key_rlc).")
        file = AESEncryption.decrypt_bytes_file(self.file, key)
        file.seek(0)
        return file

    def delete_on_cloud(self) -> None:
        key = self.get_encrypted_file_key()
        default_storage.delete(key)

    def download(self, aes_key):
        key = self.get_encrypted_file_key()
        return download_and_decrypt_file(key, aes_key)

    def upload(self, file, aes_key):
        key = self.get_encrypted_file_key()
        encrypt_and_upload_file(file, key, aes_key)

    def exists_on_s3(self):
        return default_storage.exists(self.get_encrypted_file_key())
