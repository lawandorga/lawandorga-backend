# Generated by Django 3.1.7 on 2021-03-23 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_delete_useractivationlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, default=None, max_length=17, null=True),
        ),
    ]
