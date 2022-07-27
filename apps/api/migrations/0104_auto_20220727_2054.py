# Generated by Django 3.2.14 on 2022-07-27 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0103_rename_rlcencryptionkeys_oldrlcencryptionkeys'),
    ]

    operations = [
        migrations.AddField(
            model_name='rlcuser',
            name='private_key',
            field=models.BinaryField(default=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rlcuser',
            name='private_key_encrypted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rlcuser',
            name='public_key',
            field=models.BinaryField(default=b''),
            preserve_default=False,
        ),
    ]
