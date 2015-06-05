from django.conf.urls import patterns, url, include

from meetings.views import *

def url_tree(regex, *urls):
    return url(regex, include(patterns('', *urls)))

urlpatterns = patterns('',
    url(r'^$',                    IndexView.as_view(),            name='index'),
    url(r'^create/$',             MeetingCreateView.as_view(),    name='create'),
    url_tree(r'^(?P<pk>\d+)/',
        url(r'^detail/$',         MeetingDetailView.as_view(),    name='detail'),
        url(r'^add_note/$',       AddMeetingNote.as_view(),       name='add_note'),
        url(r'^edit/$',           MeetingEditView.as_view(),      name='edit'),
        url(r'^proceedings/$',    MeetingAddNotesView.as_view(),  name='proceedings'),
    ),
)
