# Generated by Django 4.1.4 on 2023-01-01 15:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_questionnaire_folder_uuid_questionnaire_key_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionnaire",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
