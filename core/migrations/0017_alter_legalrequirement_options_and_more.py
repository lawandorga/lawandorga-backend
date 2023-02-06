# Generated by Django 4.1.4 on 2022-12-28 13:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_encryptedrecorddocument_key"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="legalrequirement",
            options={
                "ordering": ["order"],
                "verbose_name": "LegalRequirement",
                "verbose_name_plural": "LegalRequirements",
            },
        ),
        migrations.AlterModelOptions(
            name="recorddeletion",
            options={
                "ordering": ["-created"],
                "verbose_name": "RecordDeletion",
                "verbose_name_plural": "RecordDeletions",
            },
        ),
        migrations.AddField(
            model_name="legalrequirement",
            name="order",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="legalrequirement",
            name="show_on_register",
            field=models.BooleanField(default=False),
        ),
    ]
