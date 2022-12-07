# Generated by Django 4.1.3 on 2022-12-06 10:29

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0181_record_raw_folder"),
    ]

    operations = [
        migrations.AddField(
            model_name="record",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
