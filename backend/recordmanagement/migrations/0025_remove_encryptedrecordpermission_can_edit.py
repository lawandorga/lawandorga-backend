# Generated by Django 3.1.7 on 2021-03-29 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordmanagement', '0024_delete_missingrecordkey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encryptedrecordpermission',
            name='can_edit',
        ),
    ]
