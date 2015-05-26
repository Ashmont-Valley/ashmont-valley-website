# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='chair',
            field=models.ForeignKey(related_name='chair', blank=True, to='meetings.Person', help_text='chair of the meeting', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='people_attending',
            field=models.ManyToManyField(help_text='list of people who attended the meeting', related_name='people_attending', null=True, to='meetings.Person', blank=True),
            preserve_default=True,
        ),
    ]
