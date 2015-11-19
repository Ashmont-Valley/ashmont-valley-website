#
# Copyright 2015, Martin Owens <doctormo@gmail.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Provides a way to generate icon drop down from bootstrap javascript
"""

import os
from django.utils.functional import lazy

from django.db.models import CharField
from django.forms import Select, TypedChoiceField

def glyphicons():
    ret = tuple()
    for entry in get_css('css/bootstrap.min.css'):
        if entry.startswith('glyphicon-') and entry[-1] == '}':
            name = entry.split('-', 1)[-1].split(':before')[0]
            icon = entry.split('content:"')[-1].split('"')[0]
            icon = unichr(int(icon[1:], 16)).encode('utf-8')
            ret += (name, icon),
    if not ret:
        import sys
        sys.stderr.write("No icons found, Glyphicons dropdown disabled.")
    return ret
        
def get_css(cssfile):
    path = get_media(cssfile)
    if path:
        with open(path[0], 'r') as fhl:
            return fhl.read().split('.')
    return []

def get_media(path):
    from django.contrib.staticfiles import finders
    result = finders.find(path, all=True)
    return [os.path.realpath(path) for path in result]

class GlyphiconWidget(Select):
    class Media:
        css = {'all': ('css/glyphicon_field.css',)}

class GlyphiconFormField(TypedChoiceField):
    widget = GlyphiconWidget

    def widget_attrs(self, widget):
        return {'class': 'glyphicon-select'}


class GlyphiconField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = lazy(glyphicons, tuple)()
        kwargs['max_length'] = 32
        super(GlyphiconField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(GlyphiconField, self).deconstruct()
        del kwargs["choices"]
        del kwargs["max_length"]
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'choices_form_class': GlyphiconFormField}
        defaults.update(kwargs)
        return super(GlyphiconField, self).formfield(**defaults)

