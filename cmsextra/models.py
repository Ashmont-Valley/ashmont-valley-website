#
# Copyright 2014, Martin Owens <doctormo@gmail.com>
#
# This file is part of the software inkscape-web, consisting of custom 
# code for the Inkscape project's django-based website.
#
# inkscape-web is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# inkscape-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with inkscape-web.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from django.db.models import *
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from cms.models import CMSPlugin
from hoodcms.fields import ResizedImageField

from .glyphicons import GlyphiconField

null = dict(null=True, blank=True)

class Carousel(CMSPlugin):
    pass

class CarouselItem(CMSPlugin):
    caption = CharField(max_length=255)
    image   = ResizedImageField(max_width=1900, max_height=1080, upload_to='carousel')


class PannelRow(CMSPlugin):
    title = CharField(max_length=255)

class Pannel(CMSPlugin):
    title = CharField(max_length=32)
    desc  = CharField(max_length=255)
    link  = URLField(**null)
    icon  = GlyphiconField(default='thumbs-down')

class PortfolioSection(CMSPlugin):
    title = CharField(max_length=255)

class PortfolioItem(CMSPlugin):
    title = CharField(max_length=64, **null)
    link = URLField(**null)
    image = ResizedImageField(max_width=700, max_height=450, upload_to='portfolio')


class CallToAction(CMSPlugin):
    link = URLField()


class HorizontalRule(CMSPlugin):
    pass


class EmbededSvg(CMSPlugin):
    svg_file = FileField(upload_to='embeded_svg')


