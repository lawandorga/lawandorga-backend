# Generated by Django 3.2.10 on 2022-01-03 18:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recordmanagement', '0110_remove_encryptedrecorddeletionrequest_old_record'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EncryptedRecordDeletionRequest',
            new_name='RecordDeletion',
        ),
    ]