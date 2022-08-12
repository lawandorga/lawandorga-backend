# Generated by Django 3.2.11 on 2022-02-12 23:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0088_remove_group_note"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="from_rlc",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="group_from_rlc",
                to="core.rlc",
            ),
        ),
    ]