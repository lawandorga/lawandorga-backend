# Generated by Django 3.1.6 on 2021-05-12 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0060_auto_20210512_1854"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
