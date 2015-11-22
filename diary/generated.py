
from django.utils.timezone import now
from calendar import monthcalendar as cal, firstweekday, month_name, day_name
from datetime import *
from time import *

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.utils.dateformat import format as fmtdate
from .models import *

def spaced_property(f):
    def _inner(*args, **kwargs):
        return ' '.join(list(f(*args, **kwargs)))
    return _inner

def ym(year, month):
    """Roll over the month, so years go up and down as needed"""
    return [year + (month-1) / 12, (month-1) % 12 + 1]

class Generated(list):
    """Contains events with non-event elements"""
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.init(**kwargs)

    def get_calendar(self):
        if 'calendar' in self.kwargs:
            return Calendar.objects.get(slug=self.kwargs['calendar'])

class DayCalendar(Generated):
    """Contains a list of events for this day"""
    def init(self, year, month, day, **kwargs):
        self.date = date(int(year), int(month), int(day))
        self.inner = self.kwargs.pop('inner', True)

    def __str__(self):
        return fmtdate(self.date, 'jS')

    def __int__(self):
        return self.date.day

    def get_absolute_url(self):
        return reverse('diary:day', kwargs=self.kwargs)

    @property
    def parent(self):
        kwargs = self.kwargs.copy()
        kwargs.pop('day')
        return MonthCalendar(**kwargs)

    def is_today(self):
        import pytz
        EST = pytz.timezone("America/New_York")
        return cmp(now().astimezone(EST).date(), self.date)

    @spaced_property
    def get_css(self):
        yield 'cal-month-day'
        if self.inner:
            yield 'cal-day-'+['today', 'past', 'future'][self.is_today()]
            yield 'cal-day-inmonth'
        else:
            yield 'cal-day-outmonth'

        if self.date.weekday() > 4:
            yield 'cal-weekend'


class MonthCalendar(Generated):
    """A list of days iterable by week"""
    def init(self, year, month, **kwargs):
        self.year = int(year)
        self.month = int(month)
        self.days = {}
        self.load_month(self.year, self.month)

    def __str__(self):
        return month_name[int(self.month)]

    def __int__(self):
        return self.month

    @property
    def parent(self):
        kwargs = self.kwargs.copy()
        kwargs.pop('month')
        return YearCalendar(**kwargs)

    def get_absolute_url(self):
        return reverse('diary:month', kwargs=self.kwargs)

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
                kwargs = self.kwargs.copy()
                kwargs.update(dict(year=year, month=month, day=day))
                self[week_id][day_id] = DayCalendar(inner=inner, **kwargs)
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


class YearCalendar(Generated):
    def init(self, year, **kwargs):
        self.year = int(year)
        for x in range(12):
            self.append(x+1)

    def __str__(self):
        return str(self.year)

    def __int__(self):
        return self.year

    @property
    def parent(self):
        if 'calendar' in self.kwargs:
            return self.get_calendar()
        return Calendar.parent

    def get_absolute_url(self):
        return reverse('diary:year', kwargs=self.kwargs)

