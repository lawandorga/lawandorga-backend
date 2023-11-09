# Generated by Django 4.2.5 on 2023-11-02 14:08

import uuid

from django.db import migrations, models


def migrate_uuids(apps, schema_editor):
    Group = apps.get_model("core", "Group")
    for group in list(Group.objects.all()):
        group.uuid = uuid.uuid4()
        group.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0072_alter_group_keys"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=False),
        ),
        migrations.RunPython(migrate_uuids),
        migrations.AlterField(
            model_name="group",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]