# Generated by Django 2.2.2 on 2019-12-03 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recordmanagement', '0006_recorddeletionrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recorddeletionrequest',
            name='record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deletions_requested', to='recordmanagement.Record'),
        ),
    ]
