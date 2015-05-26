from django.forms import ModelForm

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
    chair = models.ForeignKey(Person, related_name="chair",
        help_text=_("chair of the meeting"), blank=True, null=True)

    class Meta:
        model = Meeting
        fields = ['start_time', 'end_time', 'chair', 'secretary',
            'people_attending', 'people_absent', 'people_guests']#,'notes']
