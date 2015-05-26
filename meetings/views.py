from django.views import generic
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _
from meetings.models import *

import datetime

class IndexView(generic.ListView):
    model = Meeting
    context = {'time_now':datetime.datetime.now()}

class MeetingDetailView(generic.DetailView):
    model = Meeting

class MeetingCreateView(generic.edit.FormView):
    form_class = MeetingCreateForm
    template_name_suffix = '_create_form'
    success_url = reverse('meetings:meeting_index')

class MeetingEditView(generic.edit.FormView):
    form_class = MeetingEditForm
    template_name_suffix='_edit_form'
    success_url = reverse('meetings:meeting_index')


