#  law&orga - record and organization management software for refugee law clinics
#  Copyright (C) 2019  Dominik Walser
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>

# Generated by Django 2.2 on 2019-04-14 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordmanagement', '0003_auto_20190411_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='state',
            field=models.CharField(choices=[('op', 'open'), ('cl', 'closed'), ('wa', 'waiting'), ('wo', 'working')], max_length=2),
        ),
    ]
