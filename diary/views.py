
from django.utils.translation import ugettext_lazy as _
from django.views.generic import *
from django.core.urlresolvers import reverse

from .mixins import AccessMixin, GeneratedObjectView
from .generated import MonthCalendar

class MonthlyCalendar(AccessMixin, GeneratedObjectView):
    model = MonthCalendar

