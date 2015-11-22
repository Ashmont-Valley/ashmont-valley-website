#
# Copyright 2015, Martin Owens <doctormo@gmail.com>
#
# This file is part of the software inkscape-web, consisting of custom 
# code for the Inkscape project's django-based website.
#
# inkscape-web is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# inkscape-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with inkscape-web.  If not, see <http://www.gnu.org/licenses/>.
#

from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, CreateView, ListView
from django.utils.translation import ugettext_lazy as _

class CsrfWhenCaching(object):
    """
    We need to add the csrf token back in when a cms page is cached.
    """
    def process_response(self, request, response):
        if type(response).__name__ == 'HttpResponse':
            request.META["CSRF_COOKIE_USED"] = True
        return response

class AutoBreadcrumbMiddleware(object):
    """
    This middleware controls and inserts some breadcrumbs
    into most pages. It attempts to navigate object hierachy
    to find the parent 
    """
    def process_template_response(self, request, response):
        if not hasattr(response, 'context_data'):
            return response
        if 'breadcrumbs' not in response.context_data:
            out = {}
            for name in ('object', 'object_list', 'parent', 'action', 'view'):
                if name in response.context_data:
                    out[name] = response.context_data[name]
            if not out.get('action', None) and 'view' in out:
                out['action'] = self._action(out['view'])
            response.context_data['breadcrumbs'] = self._crumbs(**out)
        return response

    def _crumbs(self, action=None, **kwargs):
        yield (reverse('pages-root'), _('Home'))
        target = kwargs.get('object', kwargs.get('parent',
            kwargs.get('object_list', None)))
        if kwargs.get('view', None) and hasattr(kwargs['view'], 'breadcrumbs'):
            for crumb in kwargs['view'].breadcrumbs:
                yield crumb
        elif target is not None:
            for obj in self._ancestors(target):
                if hasattr(obj, 'get_absolute_url'):
                    yield (obj.get_absolute_url(), self._name(obj))
                else:
                    yield (None, self._name(obj))

        if action is not None:
            yield (None, _(action))

    def _action(self, view):
        if hasattr(view, 'action_name'):
            return getattr(view, 'action_name')
        elif isinstance(view, UpdateView):
            return _("Edit")
        elif isinstance(view, CreateView):
            return _("New")
        elif isinstance(view, ListView):
            return _("List")

    def _ancestors(self, obj):
        if hasattr(obj, 'parent') and obj.parent:
            for parent in self._ancestors(obj.parent):
                yield parent
        yield obj

    def _name(self, obj):
        if hasattr(obj, 'breadcrumb_name'):
            return obj.breadcrumb_name()
        elif hasattr(obj, 'name'):
            return obj.name
        return unicode(obj)

