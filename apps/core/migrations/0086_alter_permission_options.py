# Generated by Django 3.2.11 on 2022-02-10 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0085_permission_recommended_for"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="permission",
            options={
                "ordering": ["name"],
                "verbose_name": "Permission",
                "verbose_name_plural": "Permissions",
            },
        ),
    ]
