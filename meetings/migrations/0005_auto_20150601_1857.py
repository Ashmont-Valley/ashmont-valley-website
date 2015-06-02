# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_auto_20150529_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='people_late',
            field=models.ManyToManyField(help_text='list of pople who arrived late at the meeting', related_name='people_late', null=True, to='meetings.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='note',
            name='name',
            field=models.CharField(help_text='name of the note', max_length=100),
            preserve_default=True,
        ),
    ]
