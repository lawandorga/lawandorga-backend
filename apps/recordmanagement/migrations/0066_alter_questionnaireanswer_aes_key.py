# Generated by Django 3.2.9 on 2021-11-26 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0065_questionnaireanswer_aes_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionnaireanswer",
            name="aes_key",
            field=models.BinaryField(default=b""),
        ),
    ]