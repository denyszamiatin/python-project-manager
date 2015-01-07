# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0005_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='developer',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
