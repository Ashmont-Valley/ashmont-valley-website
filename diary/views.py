
import calendar
from datetime import *
from time import *

from django.views.generic import *
from django.core.urlresolvers import reverse
from django.views.generic.edit import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.contrib import messages
from django.shortcuts import redirect

from hoodcms.mixins import AccessMixin

from .models import *

WEEKS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def spaced_property(f):
    def _inner(*args, **kwargs):
        return ' '.join(list(f(*args, **kwargs)))
    return _inner

class CalendarDay(list):
    """Contains a list of events for this day"""
    def __init__(self, year, month, day):
        self.name = day or ''
        self.date = None
        if day > 0:
            self.date = date(year, month, day)

    def is_today(self):
        if not self.date:
            return 1
        return cmp(now().date(), self.date)

    @spaced_property
    def get_css(self):
        yield 'cal-'+['today', 'past', 'future'][self.is_today()]
        yield 'cal-day-'+['outmonth', 'inmonth'][bool(self.date)]
        if self.date and self.date.weekday() > 4:
            yield 'cal-day-weekend'


class MonthCalendar(list):
    """A list of days iterable by week"""
    def __init__(self, year, month):
        self.days = {}
        self.year = year
        self.month = month
        for week in calendar.monthcalendar(year, month):
            self.append([])
            for day in week:
                self[-1].append(CalendarDay(year, month, day))
                if day > 0:
                    self.days[day] = self[-1][-1]

    def add_events(self, events):
        for event in events:
            date = event.date
            if event.date.year == self.year \
              and event.date.month == self.month:
                self.days[event.date.day].append(event)

    @property
    def week_days(self):
        monday = calendar.firstweekday()
        return WEEKS[monday:] + WEEKS[:monday]


class MonthlyCalendar(AccessMixin, ListView):
    template_name = 'diary/monthly.html'
    model = Event

    def get_calendar(self):
        calendar = self.kwargs.get('calendar', None)
        if calendar:
            return Calendar.objects.get(slug=calendar)

    def get_events(self, year, month):
        qs = self.get_queryset().filter(date__year=year, date__month=month)
        calendar = self.get_calendar()
        if calendar:
            qs = qs.filter(calendar=calendar)
        return qs

    @property
    def breadcrumbs(self):
        year  = int(self.kwargs.get('year', now().year))
        kwargs = {}
        yield (reverse('diary:calendar'), _('Events'))
        cal = self.get_calendar()
        if cal:
            kwargs['calendar'] = cal.slug
            yield (reverse('diary:calendar', kwargs=kwargs), unicode(cal))
        kwargs['year'] = year
        yield (reverse('diary:calendar', kwargs=kwargs), str(year))

    @property
    def action_name(self):
        month = int(self.kwargs.get('month', now().month))
        return calendar.month_name[month]

    def get_context_data(self, **kwargs):
        data  = {}
        year  = int(self.kwargs.get('year', now().year))
        month = int(self.kwargs.get('month', now().month))
        data['object'] = MonthCalendar(year, month)
        data['object'].add_events(self.get_events(year, month))
        data['view'] = self
        return data

