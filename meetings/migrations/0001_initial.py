# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_auto_20150724_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='name of the meeting', max_length=100)),
                ('meeting_date', models.DateField(help_text='date on which the meeting took place')),
                ('start_time', models.TimeField(help_text='time at which the meeting started', null=True, blank=True)),
                ('end_time', models.TimeField(help_text='time at which the meeting ended', null=True, blank=True)),
                ('chair', models.ForeignKey(related_name='chair', blank=True, to='person.Person', help_text='chair of the meeting', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(help_text='text of the note')),
                ('time_created', models.DateTimeField(help_text='time at which the note was created', auto_now_add=True)),
                ('time_edited', models.DateTimeField(help_text='time at which the note was last edited', auto_now=True)),
                ('meeting', models.ForeignKey(related_name='notes', to='meetings.Meeting', help_text='meeting that the note is for')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_type',
            field=models.ForeignKey(related_name='meetings', to='meetings.Type', help_text='type of the meeting'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='people_absent',
            field=models.ManyToManyField(help_text='list of people who were absent from the meeting', related_name='people_absent', null=True, to='person.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='people_attending',
            field=models.ManyToManyField(help_text='list of people who attended the meeting', related_name='people_attending', null=True, to='person.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='people_guests',
            field=models.ManyToManyField(help_text='list of people who were guests at the meeting', related_name='people_guests', null=True, to='person.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='people_late',
            field=models.ManyToManyField(help_text='list of pople who arrived late at the meeting', related_name='people_late', null=True, to='person.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='secretary',
            field=models.ForeignKey(related_name='secretary', blank=True, to='person.Person', help_text='secretary of the meeting', null=True),
            preserve_default=True,
        ),
    ]
