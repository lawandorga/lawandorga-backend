# Generated by Django 3.1.6 on 2021-10-06 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0070_remove_userprofile_email_confirmed"),
    ]

    operations = [
        migrations.DeleteModel(
            name="NewUserRequest",
        ),
    ]