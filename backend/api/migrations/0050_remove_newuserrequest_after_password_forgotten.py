# Generated by Django 3.1.7 on 2021-03-26 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0049_userprofile_locked"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="newuserrequest", name="after_password_forgotten",
        ),
    ]
