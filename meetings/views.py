from django.views.generic import *
from django.core.urlresolvers import reverse
from django.views.generic.edit import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from meetings.models import *
from person.models import *
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
    model = User
    permissions = ['meetings.change_meeting']
    template_name = 'generic_form.html'
    fields = ['first_name', 'last_name']

    def post(self, request):
        if self.request.is_ajax():
            #the entire name is in the first_name variable
            name = (request.POST['first_name']).split(None, 1)
            first_name = name[0]
            if len(name) == 2:
                last_name = name[1]
            else:
                last_name = ""
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
        try:
            obj = Person.objects.get(auser__first_name=first_name, auser__last_name=last_name)
        except Person.DoesNotExist:
            username = self.create_username(first_name, last_name)
            auser = User(first_name=first_name, last_name=last_name, username=username)
            try: 
                #usernames need to be unique so this fails if the username is already in use
                auser.save()
            except:
                #a really dirty way to attach a unique number suffix to the username
                #with the current implementation I don't think this should ever happen
                suffix = 1
                while True:
                    try: 
                        auser.username = username + "%d" % suffix
                        auser.save()
                        break
                    except:
                        suffix += 1
            obj = Person(auser=auser)
            obj.save()
        self.object = obj
        data = {'pk': self.object.pk, 'name': self.object.auser.name()}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def create_username(self, first_name, last_name):
        first_name_exists = (first_name != None and first_name.strip != "")
        last_name_exists = (last_name != None and last_name.strip != "")
        if first_name_exists and last_name_exists:
            return first_name + " " + last_name
        if first_name_exists and not last_name_exists:
            return first_name
        if not first_name_exists and last_name_exists:
            return last_name
        return"Unspecified"

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
    form_class = NoteCreateForm
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
