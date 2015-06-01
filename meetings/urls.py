from django.conf.urls import patterns, url

from meetings.views import *

urlpatterns = patterns('',
    url(r'^$',                          IndexView.as_view(),         
                                            name='meeting_index'),
    url(r'^detail/(?P<pk>\d+)/$',       MeetingDetailView.as_view(), 
                                            name='meeting_detail'),
    url(r'^edit/(?P<pk>\d+)/$',         MeetingEditView.as_view(),   
                                            name='meeting_edit'),
    url(r'^create/$',                   MeetingCreateView.as_view(), 
                                            name='meeting_create'),
    url(r'^proceedings/(?P<pk>\d+)/$',  MeetingAddNotesView.as_view(), 
                                            name='meeting_proceedings'),
)
