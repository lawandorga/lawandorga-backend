# Generated by Django 4.1.3 on 2022-11-28 09:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0173_merge_20221128_0955"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recordupgrade",
            name="org_pk",
        ),
        migrations.AddField(
            model_name="foldersfolder",
            name="org",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="folders_folders",
                to="core.org",
            ),
        ),
        migrations.AddField(
            model_name="recordupgrade",
            name="raw_folder",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="record_upgrades",
                to="core.foldersfolder",
            ),
        ),
    ]