from django.views.generic import *
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _
from meetings.models import *
from meetings.forms import *

from datetime import *

class IndexView(ListView):
    model = Meeting

class MeetingDetailView(DetailView):
    model = Meeting

class MeetingCreateView(CreateView):
    form_class = MeetingCreateForm
    template_name = 'meetings/meeting_create_form.html'
    model = Meeting

    def get_success_url(self):
        return reverse('meetings:meeting_index')

class MeetingEditView(UpdateView):
    form_class = MeetingEditForm
    template_name = 'meetings/meeting_edit_form.html'
    model = Meeting

    def get_success_url(self):
        return reverse('meetings:meeting_index')

    def get_object(self):
        """edit view can only be accessed for meetings that have 
        happened in the past week"""
        obj = super(MeetingEditView, self).get_object()
        if obj.is_editable():
            return obj
        raise obj.DoesNotExist('Is not editable')
