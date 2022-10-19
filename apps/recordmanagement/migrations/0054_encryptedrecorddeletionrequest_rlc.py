# Generated by Django 3.1.6 on 2021-11-16 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0075_remove_userprofile_is_active"),
        ("recordmanagement", "0053_auto_20211018_1609"),
    ]

    operations = [
        migrations.AddField(
            model_name="encryptedrecorddeletionrequest",
            name="rlc",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="deletion_requests",
                to="core.rlc",
            ),
        ),
    ]