# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_note_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='meeting_type',
            field=models.ForeignKey(related_name='meetings', to='meetings.Type', help_text='type of the meeting'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='name',
            field=models.CharField(help_text='name of the meeting', max_length=100),
            preserve_default=True,
        ),
    ]
