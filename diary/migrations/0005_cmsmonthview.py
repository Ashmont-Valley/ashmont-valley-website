# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
        ('diary', '0004_auto_20151122_0647'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmsMonthView',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('offset', models.IntegerField(default=0, verbose_name='Number of months from this month.')),
                ('calendar', models.ForeignKey(blank=True, to='diary.Calendar', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
