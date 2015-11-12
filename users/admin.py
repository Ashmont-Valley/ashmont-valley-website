
from django.contrib.admin import *
from django.contrib.sessions.models import Session

from .forms import UserForm
from .models import *

class PersonAdmin(ModelAdmin):
    form = UserForm
    fieldsets = [
        ('Login', {'fields': ['username', 'password1', 'password2']}),
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email', 'phone', 'ophone']}),
        ('Biography', {'fields': ['photo', 'desc']}),
        (None, {'fields': ['ctype', 'org']}),
        (None, {'fields': ['notes']}),
    ]

site.register(Person, PersonAdmin)
site.register(ContactType)

site.register(Address)
site.register(Country)
site.register(State)
site.register(City)
site.register(Road)
site.register(Building)


