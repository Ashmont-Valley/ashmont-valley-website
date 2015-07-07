# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0007_auto_20150626_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='chair',
            field=models.ForeignKey(related_name='chair', blank=True, to='person.Person', help_text='chair of the meeting', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='people_absent',
            field=models.ManyToManyField(help_text='list of people who were absent from the meeting', related_name='people_absent', null=True, to='person.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='people_attending',
            field=models.ManyToManyField(help_text='list of people who attended the meeting', related_name='people_attending', null=True, to='person.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='people_guests',
            field=models.ManyToManyField(help_text='list of people who were guests at the meeting', related_name='people_guests', null=True, to='person.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='people_late',
            field=models.ManyToManyField(help_text='list of pople who arrived late at the meeting', related_name='people_late', null=True, to='person.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='secretary',
            field=models.ForeignKey(related_name='secretary', blank=True, to='person.Person', help_text='secretary of the meeting', null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
