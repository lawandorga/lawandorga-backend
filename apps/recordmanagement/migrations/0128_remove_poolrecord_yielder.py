# Generated by Django 3.2.10 on 2022-01-07 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0127_auto_20220107_1806"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="poolrecord",
            name="yielder",
        ),
    ]
