# Generated by Django 5.0.8 on 2024-09-26 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0121_alter_mailattachment_mail_import"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mailattachment",
            name="file_location",
        ),
    ]