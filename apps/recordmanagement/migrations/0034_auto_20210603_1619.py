# Generated by Django 3.1.6 on 2021-06-03 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0033_auto_20210517_2242"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encryptedrecorddocument",
            name="file_size",
            field=models.BigIntegerField(null=True),
        ),
    ]
