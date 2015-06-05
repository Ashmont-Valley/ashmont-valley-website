from django.forms import ModelForm, Form, CharField

from django.utils.translation import ugettext_lazy as _

from meetings.models import *

class MeetingCreateForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ('name', 'meeting_type', 'meeting_date')
        labels = {
                'meetings_type':_('Meeting Type')
                }

class MeetingEditForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['chair', 'secretary', 'people_attending', 
                'people_absent', 'people_guests']

class MeetingProceedingsForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['people_late']

class NoteUpdateForm(ModelForm):
    class Meta:
        model = Note
        fields = ['text', 'meeting']

