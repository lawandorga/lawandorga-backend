# Generated by Django 3.2.9 on 2021-12-25 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0090_rename_questionnairefile_questionnairetemplatefile"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="RecordQuestionnaire",
            new_name="Questionnaire",
        ),
    ]