# Generated by Django 3.1.7 on 2021-03-23 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0036_auto_20210323_1818"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email_confirmed",
            field=models.BooleanField(default=True),
        ),
    ]