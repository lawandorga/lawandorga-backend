# Generated by Django 3.2.11 on 2022-02-05 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0010_auto_20220205_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='collabdocument',
            name='new_id',
            field=models.IntegerField(null=True),
        ),
    ]
