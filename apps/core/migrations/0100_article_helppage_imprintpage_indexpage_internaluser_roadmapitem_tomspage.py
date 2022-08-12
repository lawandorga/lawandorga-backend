# Generated by Django 3.2.14 on 2022-07-26 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0099_usersrlckeys_correct'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manual', models.FileField(upload_to='internal/helppage/manual/', verbose_name='Manual')),
            ],
            options={
                'verbose_name': 'HelpPage',
                'verbose_name_plural': 'HelpPage',
            },
        ),
        migrations.CreateModel(
            name='ImprintPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField()),
            ],
            options={
                'verbose_name': 'ImprintPage',
                'verbose_name_plural': 'ImprintPage',
            },
        ),
        migrations.CreateModel(
            name='IndexPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField()),
            ],
            options={
                'verbose_name': 'IndexPage',
                'verbose_name_plural': 'IndexPage',
            },
        ),
        migrations.CreateModel(
            name='RoadmapItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateField()),
            ],
            options={
                'verbose_name': 'RoadmapItem',
                'verbose_name_plural': 'RoadmapItems',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='TomsPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField()),
            ],
            options={
                'verbose_name': 'TomsPage',
                'verbose_name_plural': 'TomsPage',
            },
        ),
        migrations.CreateModel(
            name='InternalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='internal_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'InternalUser',
                'verbose_name_plural': 'InternalUsers',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('content', tinymce.models.HTMLField()),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                             to='core.internaluser')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ['-date'],
            },
        ),
    ]