# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import person.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='auser',
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=person.fields.AutoOneToOneField(related_name='details', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
