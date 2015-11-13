#
# Copyright 2015, Martin Owens <doctormo@gmail.com>
#

import os
from django.utils.functional import lazy

def glyphicons():
    ret = tuple()
    path = get_media('css/bootstrap.min.css')
    if path:
        with open(path[0], 'r') as fhl:
            for entry in fhl.read().split('.'):
                if entry.startswith('glyphicon-') and entry[-1] == '}':
                    name = entry.split('-', 1)[-1].split(':before')[0]
                    icon = entry.split('content:"')[-1].split('"')[0]
                    icon = unichr(int(icon[1:], 16)).encode('utf-8')
                    ret += (name, icon),
    return ret
        

def get_media(path):
    from django.contrib.staticfiles import finders
    result = finders.find(path, all=True)
    return [os.path.realpath(path) for path in result]

GLYPHICON_CHOICES = lazy(glyphicons, tuple)()

