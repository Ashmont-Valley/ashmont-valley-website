from django.views.generic import *
from django.core.urlresolvers import reverse
from django.views.generic.edit import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from meetings.models import *
from meetings.forms import *
from django.contrib import messages
from django.shortcuts import redirect

from datetime import *
from time import *

class IndexView(ListView):
    model = Meeting

    def get_queryset(self):
        return Meeting.objects.order_by('-meeting_date', 'name')

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
        return reverse('meetings:index')

class AddMeetingNote(CreateView):
    template_name = 'meetings/note.html'
    model = Note
    form_class = NoteUpdateForm

    def form_valid(self, form):
        messages.warning(self.request, 'You have successfully created a new note')
        if self.request.is_ajax():
            obj = form.save()
            return self.render_to_response({ 'note': obj })
        return super(AddMeetingNote, self).form_valid(form)

    def get_meeting(self):
        return Meeting.objects.get(pk=self.kwargs['pk'])

    def form_invalid(self, form):
        messages.warning(self.request, 'The submitted form was invalid')
        return redirect(reverse('meetings:proceedings', args=[self.get_meeting().pk]))

    def get_success_url(self):
        return reverse('meetings:proceedings', args=[self.get_meeting().pk])

class DeleteMeetingNote(DeleteView):
    model = Note
    
    def get_success_url(self):
        return reverse('meetings:proceedings', args=[self.get_meeting().pk])

class UpdateMeetingNote(UpdateView):
    form_class = NoteUpdateForm
    template_name = 'meetings/note.html'
    model = Note

class MeetingCreateView(CreateView):
    form_class = MeetingCreateForm
    template_name = 'meetings/meeting_create_form.html'
    model = Meeting

    def get_success_url(self):
        obj = self.object
        if obj.is_editable(): 
            return reverse('meetings:edit', args=[obj.pk])
        return reverse('meetings:detail', args=[obj.pk])

class MeetingEditView(UpdateView):
    form_class = MeetingEditForm
    template_name = 'meetings/meeting_edit_form.html'
    model = Meeting

    def form_valid(self, form):
        obj = self.object
        obj.start_time = datetime.now()
        return super(MeetingEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse('meetings:proceedings', args=[self.object.pk])

    def get_object(self):
        """edit view can only be accessed for meetings that have 
        happened in the past week"""
        obj = super(MeetingEditView, self).get_object()
        if obj.is_editable():
            return obj
        raise obj.DoesNotExist('Is not editable')

