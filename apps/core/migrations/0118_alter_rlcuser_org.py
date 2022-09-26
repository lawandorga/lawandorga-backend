# Generated by Django 4.0.7 on 2022-09-26 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0117_rlcuser_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rlcuser',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='users', to='core.org'),
        ),
    ]
