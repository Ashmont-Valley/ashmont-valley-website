# -*- coding: utf-8 -*-
#
# Copyright 2013, Martin Owens <doctormo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView as AV, RegistrationView

from .views import *
from .forms import RegisForm, PasswordForm

def url_tree(regex, view='', *urls):
    return url(regex, include(patterns(view, *urls)))

AC = TemplateView.as_view(template_name='registration/activation_complete.html')
RC = TemplateView.as_view(template_name='registration/registration_complete.html')
RK = TemplateView.as_view(template_name='registration/registration_closed.html')
RG = RegistrationView.as_view(form_class=RegisForm)
UIDB = r'^(?P<uidb64>.+?)/(?P<token>.+)/$'

# Our user url implementation allows other urls files to add
# their own urls to our user tree. Creating user functions.
USER_URLS = url_tree(r'^~(?P<username>[^\/]+)', 'users.views',
  url(r'^/?$',                    ProfileView.as_view(), name='view_profile'),
  url(r'^/friend/$',              MakeFriend.as_view(),  name='user_friend'),
  url(r'^/unfriend/$',            LeaveFriend.as_view(), name='user_unfriend'),
)

urlpatterns = patterns('',
  url(r'^', include('social_auth.urls')),
  url_tree(r'^user/', 'django.contrib.auth.views',
    url(r'^login/',     'login',                 name='auth_login'),
    url(r'^logout/',    'logout',                name='auth_logout'),
    url_tree(r'^pwd/', 'django.contrib.auth.views',
      url(r'^$',      'password_reset', {'password_reset_form': PasswordForm }, name='password_reset'),
      url(UIDB,       'password_reset_confirm',  name='password_reset_confirm'),
      url(r'^done/$', 'password_reset_complete', name='password_reset_complete'),
      url(r'^sent/$', 'password_reset_done',     name='password_reset_done'),
    ),

    url_tree(r'^register/', '',
      url(r'^$',                         RG,           name='auth_register'),
      url(r'^complete/$',                RC,           name='registration_complete'),
      url(r'^closed/$',                  RK,           name='registration_disallowed'),
      url(r'^activate/(?P<activation_key>\w+)/$', AV.as_view(), name='registration_activate'),
      url(r'^activated/$',               AC,           name='registration_activation_complete'),
    ),
  ),
  url_tree(r'', 'users.views',
    url(r'^user/$',                   MyProfile.as_view(),   name='my_profile'),
    url(r'^user/edit/$',              EditProfile.as_view(), name='edit_profile'),
    url(r'^faces/$',                  FacesView.as_view(),   name='faces'),
  ),
  USER_URLS,
)
