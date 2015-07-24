from django.forms import ModelForm, Form, CharField
from ajax_select import make_ajax_field
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from meetings.models import *
from person.models import *

class MeetingCreateForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ('name', 'meeting_type', 'meeting_date')
        labels = {
                'meetings_type':_('Meeting Type')
                }

class MeetingAjaxForm(ModelForm):
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
        js = ('js/add_person.js',)

class MeetingReeditForm(MeetingAjaxForm):
    people_late = make_ajax_field(Meeting, 'people_late', 'person_lookup')

    class Meta:
        model = Meeting
        fields = ['name', 'meeting_type', 'chair', 'secretary', 'people_attending', 
                'people_absent', 'people_guests', 'people_late']

    class Media:
        js = ('js/add_person.js', 'js/meetings.js')

class MeetingProceedingsForm(ModelForm):
    people_late = make_ajax_field(Meeting, 'people_late', 'person_lookup')

    class Meta:
        model = Meeting
        fields = ['people_late']

    class Media:
        js = ('js/add_person.js', 'js/meetings.js')

class CreatePersonForm(ModelForm):
    
    class Meta:
        model = User
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

class NoteUpdateForm(ModelForm):
    class Meta:
        model = Note
        fields = ['text']

class NoteCreateForm(ModelForm):
    class Meta:
        model = Note
        fields = ['text', 'meeting']
