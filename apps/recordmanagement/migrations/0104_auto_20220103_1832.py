# Generated by Django 3.2.10 on 2022-01-03 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordmanagement', '0103_encryptedrecorddeletionrequest_record'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='encryptedrecorddeletionrequest',
            options={'ordering': ['-state', '-created'], 'verbose_name': 'EncryptedRecordDeletionRequest', 'verbose_name_plural': 'EncryptedRecordDeletionRequests'},
        ),
        migrations.RenameField(
            model_name='encryptedrecorddeletionrequest',
            old_name='requested',
            new_name='created',
        ),
    ]
