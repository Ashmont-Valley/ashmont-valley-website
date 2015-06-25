from django.forms import ModelForm, Form, CharField
from ajax_select import make_ajax_field
from django.utils.translation import ugettext_lazy as _

from meetings.models import *

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

class NoteUpdateForm(ModelForm):
    class Meta:
        model = Note
        fields = ['text', 'meeting']

