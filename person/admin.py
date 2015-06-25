
from django.contrib.admin import *
from django.contrib.sessions.models import Session

from .forms import PersonAdminForm
from .models import *

class PersonAdmin(ModelAdmin):
    form = PersonAdminForm
    fieldsets = [
        ('Personal Information', {'fields': ['first_name', 'last_name', 'phone', 'ophone', 'email',]}),
        ('Biography', {'fields': ['photo', 'desc', 'notes']}),
        (None, {'fields': ['ctype', 'org']}),
    ]

site.register(Person, PersonAdmin)
site.register(ContactType)

site.register(Address)
site.register(Country)
site.register(State)
site.register(City)
site.register(Road)
site.register(Building)


