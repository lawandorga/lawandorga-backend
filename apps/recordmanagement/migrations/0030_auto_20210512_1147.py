# Generated by Django 3.1.6 on 2021-05-12 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordmanagement', '0029_auto_20210508_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptedrecord',
            name='last_edited',
            field=models.DateTimeField(auto_now=True),
        ),
    ]