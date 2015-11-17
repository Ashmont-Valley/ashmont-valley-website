
from django.contrib.admin import *
from .models import *

site.register(Calendar)
site.register(EventTemplate)
site.register(TaskTemplate)
site.register(Event)
site.register(Task)
site.register(Alert)

