# Generated by Django 4.1.2 on 2022-11-08 13:25

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0145_alter_foldersfolder_org_pk"),
    ]

    operations = [
        migrations.AddField(
            model_name="rlcuser",
            name="slug",
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]