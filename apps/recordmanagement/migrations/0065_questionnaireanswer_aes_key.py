# Generated by Django 3.2.9 on 2021-11-26 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0064_alter_questionnaireanswer_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="questionnaireanswer",
            name="aes_key",
            field=models.BinaryField(blank=True, null=True),
        ),
    ]