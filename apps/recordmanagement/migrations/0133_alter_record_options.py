# Generated by Django 3.2.12 on 2022-03-02 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0132_auto_20220302_1623"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="record",
            options={
                "ordering": ["-created"],
                "verbose_name": "Record",
                "verbose_name_plural": "Records",
            },
        ),
    ]