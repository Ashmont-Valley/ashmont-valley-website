from meetings.models import *
from meetings.forms import MeetingAdminForm
from django.contrib import admin
from django.forms.widgets import TextInput


class NotesInline(admin.TabularInline):
    model = Note 
    extra = 2
    formfield_overrides = {
        models.TextField: {'widget': TextInput(attrs={'size':'150'})},
    }

class MeetingAdmin(admin.ModelAdmin):
    form = MeetingAdminForm
    fieldsets = [
        ('Meeting Name', {'fields':['name']}),
        ('Meeting Type', {'fields':['meeting_type']}),
        ('Date and Time of Meeting', {'fields':['meeting_date',
                                       'start_time','end_time']}),
        ('Chairman of Meeting', {'fields':['chair']}),
        ('Secretary of Meeting', {'fields':['secretary']}),
        ('People Attending', {'fields':['people_attending']}),
        ('People Absent', {'fields':['people_absent']}),
        ('Guests', {'fields':['people_guests']}),
        ]
    list_display = ('name', 'meeting_date', 'chair','secretary')
    inlines= [NotesInline]
    search_fields = ['name', 'meeting_date', 'chair', 'secretary']
    list_filter = ['meeting_date', 'meeting_type']

class TypeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name of Type', {'fields':['name']}),
        ]

class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['name']}),
        ]

admin.site.register(Type, TypeAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Meeting, MeetingAdmin)
