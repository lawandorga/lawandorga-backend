# Generated by Django 3.1.7 on 2021-03-23 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_userprofile_email_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivationlink',
            name='link',
            field=models.CharField(auto_created=True, default='default', max_length=32, unique=True),
        ),
    ]
