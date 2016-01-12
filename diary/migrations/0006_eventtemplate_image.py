# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0005_cmsmonthview'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtemplate',
            name='image',
            field=models.ImageField(null=True, upload_to=b'diary/event_template', blank=True),
            preserve_default=True,
        ),
    ]
