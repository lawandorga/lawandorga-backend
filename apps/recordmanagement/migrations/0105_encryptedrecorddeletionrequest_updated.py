# Generated by Django 3.2.10 on 2022-01-03 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0104_auto_20220103_1832"),
    ]

    operations = [
        migrations.AddField(
            model_name="encryptedrecorddeletionrequest",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]