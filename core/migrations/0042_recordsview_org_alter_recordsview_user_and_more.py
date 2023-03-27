# Generated by Django 4.1.7 on 2023-03-27 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0041_alter_recordsdeletion_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="recordsview",
            name="org",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="records_views",
                to="core.org",
            ),
        ),
        migrations.AlterField(
            model_name="recordsview",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="records_views",
                to="core.rlcuser",
            ),
        ),
        migrations.AddConstraint(
            model_name="recordsview",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("org__isnull", True), ("user__isnull", False)),
                    models.Q(("org__isnull", False), ("user__isnull", True)),
                    _connector="OR",
                ),
                name="records_view_one_of_both_is_set",
            ),
        ),
    ]