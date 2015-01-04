# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0003_userrole'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('roles', models.CharField(max_length=200)),
                ('project', models.ForeignKey(to='project_manager.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.CharField(max_length=32),
        ),
    ]
