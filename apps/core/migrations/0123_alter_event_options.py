# Generated by Django 3.2.15 on 2022-10-19 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0122_merge_20221004_1650'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_time']},
        ),
    ]
