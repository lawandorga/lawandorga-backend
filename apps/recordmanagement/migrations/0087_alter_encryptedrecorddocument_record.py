# Generated by Django 3.2.9 on 2021-12-25 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recordmanagement', '0086_encryptedrecorddocument_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptedrecorddocument',
            name='record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='recordmanagement.record'),
        ),
    ]
