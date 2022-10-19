# Generated by Django 3.2.10 on 2022-01-07 17:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recordmanagement", "0126_auto_20220105_1637"),
    ]

    operations = [
        migrations.AlterField(
            model_name="poolconsultant",
            name="consultant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="poolrecord",
            name="record",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recordmanagement.record",
            ),
        ),
        migrations.AlterField(
            model_name="poolrecord",
            name="yielder",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]