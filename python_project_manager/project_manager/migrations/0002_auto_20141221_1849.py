# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0001_squashed_0007_auto_20141125_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.CharField(default=b'root', max_length=32, blank=True),
        ),
    ]
