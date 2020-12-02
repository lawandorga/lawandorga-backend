# Generated by Django 3.0 on 2020-12-02 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0020_encryptedrecorddocumentdeletionrequest_record"),
        ("collab", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecordDocument",
            fields=[
                (
                    "textdocument_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="collab.TextDocument",
                    ),
                ),
                (
                    "record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collab_documents",
                        to="recordmanagement.EncryptedRecord",
                    ),
                ),
            ],
            bases=("collab.textdocument",),
        ),
    ]
