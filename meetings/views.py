from django.views import generic
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _
from meetings.models import *
from meetings.forms import *

import datetime

class IndexView(generic.ListView):
    model = Meeting
    context = {'time_now':datetime.datetime.now(), 
        'time_cutoff':datetime.timedelta(days=7)}

class MeetingDetailView(generic.DetailView):
    model = Meeting

class MeetingCreateView(generic.CreateView):
    model = Meeting
    template_name = 'meeting_create_form.html'
    success_url = reverse('meetings:meeting_index')

class MeetingEditView(generic.EditView):
    model = Meeting
    template_name = 'meeting_edit_form.html'
    success_url = reverse('meetings:meeting_index')

#class MeetingCreateView(generic.edit.FormView):
#    form_class = MeetingCreateForm
#    template_name = 'meeting_create_form.html'
#    success_url = reverse('meetings:meeting_index')

#class MeetingEditView(generic.edit.FormView):
#    form_class = MeetingEditForm
#    template_name = 'meeting_edit_form.html'
#    success_url = reverse('meetings:meeting_index')


