from meetings.models import *
from users.models import *
from django.contrib import admin
from django.forms.widgets import TextInput
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import autoselect_fields_check_can_add

class NotesInline(admin.TabularInline):
    model = Note 
    extra = 2
    formfield_overrides = {
            models.TextField: {'widget': TextInput(attrs={'style':'width:100%'})},
    }

class MeetingAdmin(AjaxSelectAdmin, admin.ModelAdmin):
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
        ('People Late', {'fields':['people_late']}),
        ]
    list_display = ('name', 'meeting_date', 'chair','secretary')
    inlines= [NotesInline]
    search_fields = ['name', 'meeting_date', 'chair', 'secretary']
    list_filter = ['meeting_date', 'meeting_type']

class TypeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name of Type', {'fields':['name']}),
        ]


admin.site.register(Type, TypeAdmin)
admin.site.register(Meeting, MeetingAdmin)
