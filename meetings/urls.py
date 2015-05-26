from django.conf.urls import patterns, url

from meetings import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='meeting_index'),
    url(r'^detail/(?P<pk>\d+)/$', views.MeetingDetailView.as_view(), name='meeting_detail'),
    url(r'^edit/(?P<pk>\d+)/$', views.MeetingEditView.as_view(), name='meeting_edit'),
    url(r'^create/$', views.MeetingCreateView.as_view(), name='meeting_create'),
)
