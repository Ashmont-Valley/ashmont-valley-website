# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='name of the meeting', max_length=100, null=True, blank=True)),
                ('meeting_date', models.DateField(help_text='date on which the meeting took place')),
                ('start_time', models.TimeField(help_text='time at which the meeting started', null=True, blank=True)),
                ('end_time', models.TimeField(help_text='time at which the meeting ended', null=True, blank=True)),
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
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='the name of the person', max_length=100)),
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
            name='chair',
            field=models.ForeignKey(related_name='chair', to='meetings.Person', help_text='chair of the meeting'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_type',
            field=models.ForeignKey(related_name='meetings', to='meetings.Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='people_absent',
            field=models.ManyToManyField(help_text='list of people who were absent from the meeting', related_name='people_absent', null=True, to='meetings.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='people_attending',
            field=models.ManyToManyField(help_text='list of people who attended the meeting', related_name='people_attending', to='meetings.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='people_guests',
            field=models.ManyToManyField(help_text='list of people who were guests at the meeting', related_name='people_guests', null=True, to='meetings.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='secretary',
            field=models.ForeignKey(related_name='secretary', blank=True, to='meetings.Person', help_text='secretary of the meeting', null=True),
            preserve_default=True,
        ),
    ]
