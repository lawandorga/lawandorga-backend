# Generated by Django 4.1.4 on 2022-12-16 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_maildomain_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="record",
            name="name",
            field=models.CharField(default="-", max_length=300),
        ),
    ]
