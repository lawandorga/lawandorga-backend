# Generated by Django 3.2.10 on 2022-01-03 18:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recordmanagement", "0108_auto_20220103_1857"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encryptedrecorddeletionrequest",
            name="request_from",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="requestedrecorddeletions",
                to="core.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="encryptedrecorddeletionrequest",
            name="request_processed",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="processedrecorddeletions",
                to="core.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="encryptedrecorddeletionrequest",
            name="state",
            field=models.CharField(
                choices=[("re", "Requested"), ("gr", "Granted"), ("de", "Declined")],
                default="re",
                max_length=2,
            ),
        ),
    ]