# Generated by Django 3.2.10 on 2022-01-05 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordmanagement', '0118_rename_processed_on_recorddeletion_processed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='encryptedrecordpermission',
            old_name='request_processed',
            new_name='processed_by',
        ),
    ]