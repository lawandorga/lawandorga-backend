# Generated by Django 3.2.11 on 2022-02-12 23:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0086_alter_permission_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="group",
            name="creator",
        ),
        migrations.AlterField(
            model_name="group",
            name="from_rlc",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="group_from_rlc",
                to="core.rlc",
            ),
        ),
    ]
