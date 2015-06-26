from django.views.generic import *
from django.core.urlresolvers import reverse
from django.views.generic.edit import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from meetings.models import *
from meetings.forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from hoodcms.mixins import AccessMixin
from hoodcms.views import MultiListView
from datetime import *
from time import *
import json

class MeetingList(AccessMixin, MultiListView):
    model = Meeting
    paginate_by = 10

    def get_querysets(self):
        qs = Meeting.objects.order_by('-meeting_date', 'name')
        next_month = date.today() + timedelta(days=45)
        return [
          ('Up and Coming', qs.filter(meeting_date__gte=date.today(),
                                      meeting_date__lt=next_month)),
          ('Old Meetings', qs.filter(meeting_date__lt=date.today())),
          ('Far Future', qs.filter(meeting_date__gte=next_month)),
        ]

class MeetingDetailView(AccessMixin, DetailView):
    model = Meeting

class MeetingEditView(AccessMixin, UpdateView):
    model = Meeting
    permissions = ['meetings.change_meeting']
    form_class = MeetingCreateForm
    template_name = 'meetings/meeting_edit_form.html'

    def get_success_url(self):
        return reverse('meetings:detail', args=[self.object.pk])

class MeetingDeleteView(DeleteView):
    model = Meeting
    permissions = ['meetings.delete_meeting']

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if not self.object.start_time:
            #you can only delete meetings that haven't started yet
            self.object.delete()
            messages.success(request, "Meeting deleted.")
        else:
            messages.error(request, "Error: You can only delete meetings that haven't started yet.")
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('meetings:index')

class CreatePerson(CreateView):
    model = Person
    permissions = ['meetings.change_meeting']
    fields = ['name']
    template_name = 'generic_form.html'

    def post(self, request):
        (obj, isnew) = Person.objects.get_or_create(name=request.POST['name'])
        self.object = obj
        data = {'pk': self.object.pk, 'name': self.object.name}
        return HttpResponse(json.dumps(data), content_type="application/json")

class MeetingAddNotesView(AccessMixin, UpdateView):
    template_name = 'meetings/add_meeting_notes.html'
    form_class = MeetingProceedingsForm
    model = Meeting
    permissions = ['meetings.add_meeting']

    def form_valid(self, form):
        self.object.end_time = datetime.now()
        return super(MeetingAddNotesView, self).form_valid(form)

    def get_success_url(self):
        return reverse('meetings:detail', args=[self.object.pk])

class AddMeetingNote(CreateView, AccessMixin):
    template_name = 'meetings/note.html'
    model = Note
    form_class = NoteUpdateForm
    permissions = ['meetings.add_note']

    def form_valid(self, form):
        #messages.warning(self.request, 'You have successfully created a new note')
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

class DeleteMeetingNote(DeleteView ,AccessMixin):
    model = Note
    permissions = ['meetings.delete_note']

    def delete(self, *args, **kwargs):
        note_pk = self.get_object().pk
        response = super(DeleteMeetingNote, self).delete(*args, **kwargs)
        if self.request.is_ajax():
            return HttpResponse(str(note_pk), content_type="text/plain")
        return response

    def get_success_url(self):
        return reverse('meetings:proceedings', args=[self.get_object().meeting.pk])

# Permissions <app_name>.add|change|delete_<model_name>
class UpdateMeetingNote(AccessMixin, UpdateView):
    permissions = ['meetings.change_note']
    form_class = NoteUpdateForm
    template_name = 'meetings/note.html'
    model = Note

    def get_success_url(self):
        return reverse('meetings:proceedings', args=[self.get_object().meeting.pk])

class MeetingCreateView(CreateView, AccessMixin):
    form_class = MeetingCreateForm
    template_name = 'meetings/meeting_create_form.html'
    model = Meeting
    permissions = ['meetings.add_meeting']

    def get_success_url(self):
        obj = self.object
        return reverse('meetings:detail', args=[obj.pk])

class MeetingPrepareView(UpdateView, AccessMixin):
    form_class = MeetingPrepareForm
    template_name = 'meetings/meeting_prepare_form.html'
    model = Meeting
    permissions = ['meetings.change_meeting']

    def form_valid(self, form):
        obj = self.object
        obj.start_time = datetime.now()
        return super(MeetingPrepareView, self).form_valid(form)

    def get_success_url(self):
        return reverse('meetings:proceedings', args=[self.object.pk])

class MeetingReeditView(UpdateView, AccessMixin):
    form_class = MeetingReeditForm
    template_name = 'meetings/meeting_reedit_form.html'
    model = Meeting
    permissions = ['meetings.change_meeting']

    def get_success_url(self):
        return reverse('meetings:detail', args=[self.object.pk])
