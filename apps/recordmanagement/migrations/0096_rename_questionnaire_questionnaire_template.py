# Generated by Django 3.2.9 on 2021-12-25 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0095_alter_questionnaire_questionnaire"),
    ]

    operations = [
        migrations.RenameField(
            model_name="questionnaire",
            old_name="questionnaire",
            new_name="template",
        ),
    ]