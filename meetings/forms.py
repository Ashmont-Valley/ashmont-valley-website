from django import forms
from ajax_select import make_ajax_field
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from functools import partial

from meetings.models import *
from users.models import *

JQUERY_UI = 'cms/js/modules/jquery.ui.custom.js'

class MeetingCreateForm(forms.ModelForm):
    meeting_date = forms.DateField(widget=partial(forms.DateInput, {'class': 'datepicker'})())
    class Meta:
        model = Meeting
        fields = ('name', 'meeting_type', 'meeting_date')
        labels = {
                'meetings_type':_('Meeting Type')
                }

    class Media:
        css =  { 'all': ('css/jquery-ui.css', 'css/meetings.css')}
        js = (JQUERY_UI, 'js/date_dropdown.js',)

class MeetingAjaxForm(forms.ModelForm):
    chair = make_ajax_field(Meeting, 'chair', 'person_lookup')
    secretary = make_ajax_field(Meeting, 'secretary', 'person_lookup')
    people_attending = make_ajax_field(Meeting, 'people_attending', 'person_lookup')
    people_absent = make_ajax_field(Meeting, 'people_absent', 'person_lookup')
    people_guests = make_ajax_field(Meeting, 'people_guests', 'person_lookup')
    
class MeetingPrepareForm(MeetingAjaxForm):
    class Meta:
        model = Meeting
        fields = ['chair', 'secretary', 'people_attending', 
                'people_absent', 'people_guests']

    class Media:
        css =  { 'all': ('css/jquery-ui.css', 'css/meetings.css')}
        js = (JQUERY_UI, 'js/date_dropdown.js', 'js/add_person.js',)


class MeetingReeditForm(MeetingAjaxForm):
    people_late = make_ajax_field(Meeting, 'people_late', 'person_lookup')

    class Meta:
        model = Meeting
        fields = ['name', 'meeting_type', 'chair', 'secretary', 'people_attending', 
                'people_absent', 'people_guests', 'people_late']

    class Media:
        js = (JQUERY_UI, 'js/add_person.js', 'js/notes.js')

class MeetingProceedingsForm(forms.ModelForm):
    people_late = make_ajax_field(Meeting, 'people_late', 'person_lookup')

    class Meta:
        model = Meeting
        fields = ['people_late']

    class Media:
        css =  { 'all': ('css/jquery-ui.css', 'css/meetings.css')}
        js = (JQUERY_UI, 'js/date_dropdown.js', 'js/add_person.js', 'js/notes.js')

class CreatePersonForm(forms.ModelForm):
    
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'username']

    def clean_first_name(self):
        self.data = self.data.copy()
        name = self.cleaned_data['first_name']
        name_list = name.rsplit(' ', 1)
        first = name_list[0]
        if len(name_list) == 2:
            last = name_list[1]
        else:
            last = None
        self.data['last_name'] = last
        self.data['username'] = slugify(name)
        return first

class NoteUpdateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']

class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text', 'meeting']
