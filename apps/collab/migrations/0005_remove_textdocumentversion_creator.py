# Generated by Django 3.2.11 on 2022-02-05 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0004_alter_collabdocument_rlc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textdocumentversion',
            name='creator',
        ),
    ]
