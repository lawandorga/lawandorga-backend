# Generated by Django 3.2.14 on 2022-07-27 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0105_rename_private_key_encrypted_rlcuser_is_private_key_encrypted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rlcuser',
            name='private_key',
            field=models.BinaryField(null=True),
        ),
        migrations.AlterField(
            model_name='rlcuser',
            name='public_key',
            field=models.BinaryField(null=True),
        ),
    ]
