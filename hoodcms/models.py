
import os
import time

from django.contrib.staticfiles import finders
from django.templatetags.static import StaticNode

def get_media(path):
    result = finders.find(path, all=True)
    return [os.path.realpath(path) for path in result]

def new_url(self, context):
    """Add a query string to invalidate cached files when needed"""
    path = self.path.resolve(context)
    mtime = os.path.getmtime(get_media(path)[0])
    mkey = hex(int(str(mtime).split('.')[0][-3::-1]))[2:]
    return self.handle_simple(path + '?' + mkey)

StaticNode.url = new_url

