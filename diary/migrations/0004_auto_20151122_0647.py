# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_auto_20151117_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='desc',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default='No Name', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='template',
            field=models.ForeignKey(related_name='events', blank=True, to='diary.EventTemplate', null=True),
            preserve_default=True,
        ),
    ]
