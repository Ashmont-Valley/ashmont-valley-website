from django.views.generic import *
from django.core.urlresolvers import reverse
from django.views.generic.edit import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from meetings.models import *
from meetings.forms import *

from datetime import *
from time import *

class IndexView(ListView):
    model = Meeting

class MeetingDetailView(DetailView):
    model = Meeting

class MeetingAddNotesView(UpdateView):
    template_name = 'meetings/add_meeting_notes.html'
    form_class = MeetingProceedingsForm
    model = Meeting

    def form_valid(self, form):
        self.object.end_time = datetime.now()
        return super(MeetingAddNotesView, self).form_valid(form)

    def get_success_url(self):
        return reverse('meetings:meeting_index')

class AddMeetingNote(FormView, SingleObjectMixin):
    form_class = NoteCreationForm
    template_name = 'meetings/note.html'
    model = Meeting

#this seems to create a new note everytime the form is submitted
#should there be a separate view for moreely updating notes instead
#of creating them? Or can we do that solely with Ajax?
    def form_valid(self, form):
        obj = self.get_object().notes.create(content=self.request.POST['content'])
        return self.render_to_response({ 'note': obj })


class MeetingCreateView(CreateView):
    form_class = MeetingCreateForm
    template_name = 'meetings/meeting_create_form.html'
    model = Meeting

    def get_success_url(self):
        obj = self.object
        if obj.is_editable(): 
            return reverse('meetings:meeting_edit', args=[obj.pk])
        return reverse('meetings:meeting_detail', args=[obj.pk])

class MeetingEditView(UpdateView):
    form_class = MeetingEditForm
    template_name = 'meetings/meeting_edit_form.html'
    model = Meeting

    def form_valid(self, form):
        obj = self.object
        obj.start_time = datetime.now()
        return super(MeetingEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse('meetings:meeting_proceedings', args=[self.object.pk])

    def get_object(self):
        """edit view can only be accessed for meetings that have 
        happened in the past week"""
        obj = super(MeetingEditView, self).get_object()
        if obj.is_editable():
            return obj
        raise obj.DoesNotExist('Is not editable')

