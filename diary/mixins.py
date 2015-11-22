
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from hoodcms.mixins import AccessMixin

import re
class GeneratedObjectView(TemplateView):
    model = None

    def get_template_names(self):
        cls = self.model.__module__.split('.')[0]
        name = re.sub('([A-Z]+)', r'_\1', self.model.__name__).strip('_')
        return "%s/%s.html" % (cls, name.lower())

    def get_object(self):
        return self.model(**self.kwargs)

    def get_context_data(self, **kwargs):
        data = super(GeneratedObjectView, self).get_context_data(**kwargs)
        data['object'] = self.get_object()
        data['calendar'] = data['object'].get_calendar()
        return data

