# Generated by Django 4.1.7 on 2023-03-25 14:48

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0035_foldersfolder_name_change_disabled"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecordsRecord",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
                ),
                ("folder_uuid", models.UUIDField(db_index=True, null=True)),
                ("is_archived", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="core.org",
                    ),
                ),
            ],
            options={
                "verbose_name": "RecordsRecord",
                "verbose_name_plural": "RecordsRecord",
            },
        ),
    ]