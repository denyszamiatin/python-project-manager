# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0006_auto_20150104_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='developer',
            field=models.ForeignKey(related_name=b'developer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='employer',
            field=models.ForeignKey(related_name=b'employer', to=settings.AUTH_USER_MODEL),
        ),
    ]
