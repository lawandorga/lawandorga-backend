# Generated by Django 3.2.9 on 2021-12-25 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0076_alter_rlcuser_options"),
        ("recordmanagement", "0088_alter_encryptedrecorddocument_old_record"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Questionnaire",
            new_name="QuestionnaireTemplate",
        ),
    ]
