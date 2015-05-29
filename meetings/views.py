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

# This code doesn't yet work, it is committed to act as
# a guide for the real developer.
class AddMeetingNotes(UpdateView):
    template_name = 'meetings/add_meeting_notes.html'
    form_class = MeetingProceedingsForm
    model = Meeting

class AddMeetingNote(FormView, ObjectMixin):
    form_class = NoteCreationForm
    template_name = 'meetings/note.html'
    model = Meeting

    def on_form_valid(self):
        obj = self.get_object().notes.create(content=self.request.POST['content'])
        return self.render_to_response({ 'note': obj })


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

