
from django.utils.translation import ugettext_lazy as _
from django.views.generic import *
from django.core.urlresolvers import reverse

from .models import Calendar, Event
from .mixins import AccessMixin, GeneratedObjectView
from .generated import DayCalendar, MonthCalendar, YearCalendar

class DailyCalendar(AccessMixin, GeneratedObjectView):
    model = DayCalendar

class MonthlyCalendar(AccessMixin, GeneratedObjectView):
    model = MonthCalendar

class YearlyCalendar(AccessMixin, GeneratedObjectView):
    model = YearCalendar

class FullCalendar(AccessMixin, DetailView):
    slug_url_kwarg = 'calendar'
    action_name = None
    model = Calendar

class AllEvents(AccessMixin, ListView):
    action_name = None
    model = Event

class Event(AccessMixin, DetailView):
    model = Event

