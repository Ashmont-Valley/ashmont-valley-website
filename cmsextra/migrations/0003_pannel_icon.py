# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmsextra', '0002_embededsvg'),
    ]

    operations = [
        migrations.AddField(
            model_name='pannel',
            name='icon',
            field=models.CharField(default=b'thumbs-down', max_length=22),
            preserve_default=True,
        ),
    ]
