# Generated by Django 3.2.10 on 2022-01-03 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "recordmanagement",
            "0112_rename_request_processed_recorddeletion_processed_by",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="recorddeletion",
            old_name="request_from",
            new_name="requested_from",
        ),
    ]
