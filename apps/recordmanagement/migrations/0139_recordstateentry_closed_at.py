# Generated by Django 3.2.13 on 2022-06-26 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0138_recordaccess_explanation"),
    ]

    operations = [
        migrations.AddField(
            model_name="recordstateentry",
            name="closed_at",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]