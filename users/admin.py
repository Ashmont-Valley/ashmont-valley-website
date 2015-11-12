
from django.contrib.admin import *
from django.contrib.sessions.models import Session

from .forms import PersonAdminForm
from .models import *

class PersonAdmin(ModelAdmin):
    form = PersonAdminForm
    fieldsets = [
        ('Personal Information', {'fields': ['phone', 'ophone']}),#, 'user__first_name', 'user__last_name', 'user__email']}),
        ('Biography', {'fields': ['photo', 'desc']}),
        (None, {'fields': ['ctype', 'org']}),
        (None, {'fields': ['notes', 'user']}),
    ]

site.register(Person, PersonAdmin)
site.register(ContactType)

site.register(Address)
site.register(Country)
site.register(State)
site.register(City)
site.register(Road)
site.register(Building)


