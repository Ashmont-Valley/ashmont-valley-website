
from calendar import monthcalendar as cal, firstweekday, month_name, day_name
from datetime import *
from time import *

from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import *

def spaced_property(f):
    def _inner(*args, **kwargs):
        return ' '.join(list(f(*args, **kwargs)))
    return _inner

def ym(year, month):
    """Roll over the month, so years go up and down as needed"""
    return [year + (month-1) / 12, (month-1) % 12 + 1]

class CalendarDay(list):
    """Contains a list of events for this day"""

    def __init__(self, cal, year, month, day, week):
        self.cal = cal
        self.name = day or ''
        self.date = date(year, month, day)

    @property
    def inner(self):
        return self.cal.month == self.date.month

    def get_absolute_url(self):
        kwargs = self.cal.get_url_kwargs(day=self.date.day)
        return reverse('diary:calendar', kwargs=kwargs)

    def is_today(self):
        if not self.date:
            return 1
        return cmp(now().date(), self.date)

    @spaced_property
    def get_css(self):
        yield 'cal-month-day'
        if self.inner:
            yield 'cal-day-'+['today', 'past', 'future'][self.is_today()]
            yield 'cal-day-inmonth'
        else:
            yield 'cal-day-outmonth'

        if self.date and self.date.weekday() > 4:
            yield 'cal-weekend'


class MonthCalendar(list):
    """A list of days iterable by week"""
    def __init__(self, year, month, calendar=None):
        self.days = {}
        self.year = int(year)
        self.month = int(month)
        self.calendar = calendar
        self.load_month(self.year, self.month)

    def __str__(self):
        return month_name[int(self.month)]

    @property
    def parent(self):
        return YearCalendar(self.year, calendar=self.calendar)

    def get_absolute_url(self):
        return reverse('diary:calendar')

    def load_month(self, year, month):
        for week_id, week in enumerate(cal(year, month)):
            self.append([])
            self.add_week(year, month, week, week_id)

        self.add_week(*(ym(year, month-1) + cal(*ym(year, month-1))[-1:] + [0]))
        self.add_week(*(ym(year, month+1) + cal(*ym(year, month+1))[:1] + [-1]))

    def add_week(self, year, month, week, week_id):
        for (day_id, day) in enumerate(week):
            if day_id >= len(self[week_id]):
                self[week_id].append(None)
            if day:
                inner = month==self.month
                self[week_id][day_id] = CalendarDay(self, year, month, day, week_id)
                if inner:
                    self.days[day] = self[-1][-1]

    def add_events(self, events):
        for event in events:
            date = event.date
            if event.date.year == self.year \
              and event.date.month == self.month:
                self.days[event.date.day].append(event)

    @property
    def week_days(self):
        return list(day_name)


class YearCalendar(list):
    def __init__(self, year, calendar=None):
        self.year = year
        self.calendar = calendar
        for x in range(12):
            self.append(x+1)

    @property
    def parent(self):
        if self.calendar:
            return Calendar.objects.get(slug=self.calendar)
        return Calendar.parent

    def __str__(self):
        return str(self.year)

    def get_absolute_url(self):
        return reverse('diary:calendar')

