
from django.contrib.admin import *
from django.contrib.sessions.models import Session

from .forms import UserForm, AddressForm
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

class AddressAdmin(ModelAdmin):
    list_display = ('__str__','phone','kind')
    list_filter  = ('kind', 'building__road', 'building__road__city', 'building__road__city__state', 'building__road__city__state__country')
    form = AddressForm
    fieldsets = [ 
        (None, {'fields': ['kind', 'apt', 'number', 'name', 'road', 'city', 'postcode']}),
        ('Extra Information', {'fields': ['phone', 'importid']}),
    ]   


site.register(Address, AddressAdmin)
site.register(Country)
site.register(State)
site.register(City)

