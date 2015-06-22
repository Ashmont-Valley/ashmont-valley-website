from django.conf.urls import patterns, url, include

from meetings.views import *

def url_tree(regex, *urls):
    return url(regex, include(patterns('', *urls)))

urlpatterns = patterns('',
    url(r'^$',                    IndexView.as_view(),            name='index'),
    url(r'^create/$',             MeetingCreateView.as_view(),    name='create'),
    url(r'^create/person/$',      CreatePerson.as_view(),         name='create_person'),
    url_tree(r'^(?P<pk>\d+)/',
        url(r'^detail/$',         MeetingDetailView.as_view(),    name='detail'),
        url(r'^add_note/$',       AddMeetingNote.as_view(),       name='add_note'),
        url(r'^edit/$',           MeetingEditView.as_view(),      name='edit'),
        url(r'^proceedings/$',    MeetingAddNotesView.as_view(),  name='proceedings'),
        #the following urls use the note pk, not the meeting pk
        url(r'^delete_note/$',    DeleteMeetingNote.as_view(),    name='delete_note'),
        url(r'^update_note/$',    UpdateMeetingNote.as_view(),    name='update_note'),
    ),
)
