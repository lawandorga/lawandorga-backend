# Generated by Django 3.2.9 on 2021-12-18 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0070_auto_20211217_1743"),
    ]

    operations = [
        migrations.AddField(
            model_name="record",
            name="old_client",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="records",
                to="recordmanagement.encryptedclient",
            ),
        ),
    ]
