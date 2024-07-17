# Generated by Django 5.0.6 on 2024-07-17 08:29

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0111_collab_footer_collab_letterhead"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="collab",
            name="footer",
        ),
        migrations.RemoveField(
            model_name="collab",
            name="letterhead",
        ),
        migrations.CreateModel(
            name="Template",
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
                ("name", models.CharField(blank=True, max_length=256)),
                ("description", models.TextField(blank=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "footer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.footer",
                    ),
                ),
                (
                    "letterhead",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.letterhead",
                    ),
                ),
                (
                    "org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="templates",
                        to="core.org",
                    ),
                ),
            ],
            options={
                "verbose_name": "Template",
                "verbose_name_plural": "Templates",
            },
        ),
        migrations.AddField(
            model_name="collab",
            name="template",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.template",
            ),
        ),
    ]