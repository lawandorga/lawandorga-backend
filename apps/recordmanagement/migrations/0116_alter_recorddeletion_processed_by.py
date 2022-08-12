# Generated by Django 3.2.10 on 2022-01-03 18:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recordmanagement", "0115_alter_recorddeletion_record"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recorddeletion",
            name="processed_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="processedrecorddeletions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
