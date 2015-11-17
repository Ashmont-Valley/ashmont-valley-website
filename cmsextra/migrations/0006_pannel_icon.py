# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cmsextra.glyphicons


class Migration(migrations.Migration):

    dependencies = [
        ('cmsextra', '0005_remove_pannel_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='pannel',
            name='icon',
            field=cmsextra.glyphicons.GlyphiconField(default=b'thumbs-down'),
            preserve_default=True,
        ),
    ]
