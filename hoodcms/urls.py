from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings

urlpatterns = patterns('',
    url(r'^admin/',   include(admin.site.urls)),
    url(r'^meetings/', include('meetings.urls', namespace='meetings')),
    #url(r'^calendar/', include('happenings.urls', namespace='calendar')),
    #url(r'^',         include('cms.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

