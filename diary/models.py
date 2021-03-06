
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta
from django.db.models import *
from django.utils.text import slugify

from django.core.urlresolvers import reverse
from django.conf import settings

from .generated import ym, today, YearCalendar, MonthCalendar, DayCalendar

null = {'null':True, 'blank':True}

class Calendar(Model):
    """A collection of events for a specific calendar"""
    name   = CharField(max_length=32)
    slug   = SlugField(max_length=32, blank=True)
    owner  = ForeignKey(settings.AUTH_USER_MODEL, **null)
    public = BooleanField(default=True)

    # If events are sourced from somewhere else, then we need the url
    # where we can find those events (must be http).
    import_src = URLField(**null)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diary:calendar', kwargs={'calendar': self.slug})

    def this_month(self):
        return MonthCalendar(add_events=True, year=today().year,
                             month=today().month, calendar=self.slug)
   
    def this_day(self):
        return DayCalendar(add_events=True, year=today().year,
                          month=today().month, day=today().day, 
                          calendar=self.slug)

    @property
    def parent(self):
        return Event.objects.all()

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        return super(Calendar, self).save(**kwargs)


class EventTemplate(Model):
    """A description of an event with some default tasks""" 
    name       = CharField(max_length=64)
    desc       = TextField(**null)
    start_time = TimeField(**null)
    end_time   = TimeField(**null)
    image      = ImageField(upload_to="diary/event_template", **null)

    def __str__(self):
        return self.name

class TaskTemplate(Model):
    """A task that needs to be done every time the event is created"""
    name       = CharField(max_length=64, default='attend event')
    notes      = TextField(**null)
    template   = ForeignKey(EventTemplate, related_name='tasks')

    def __str__(self):
        return self.name


class EventQuerySet(QuerySet):
    __str__ = lambda self: "Events"

    def get_absolute_url(self):
        return reverse('diary:index')

    def calendars(self):
        """Returns a list of calendar objects"""
        pks = self.values_list('calendar_id', flat=True)
        return Calendar.objects.filter(pk__in=pks)

    def next(self):
        """Return the next three events"""
        return self.filter(date__gte=today()).order_by('-date')[:3]

    def previous(self):
        return self.filter(date__lt=today()).order_by('date')[:3]

    def upcoming(self):
        end = today() + timedelta(days=30)
        return self.filter(date__gt=today(), date__lte=end).order_by('-date')[:10]

    def recent(self):
        start = today() - timedelta(days=30)
        return self.filter(date__lt=today(), date__gte=start).order_by('date')[:10]

    def index(self):
        """Returns an indexed scheme for a tree view of events"""
        # Not complete yet XXX
        return [YearCalendar(dat.year, qs=self)
                    for dat in self.dates('date', 'year')]


class Event(Model):
    """Something that will happen on a specific date/time"""
    name       = CharField(max_length=64)
    desc       = TextField(**null)
    date       = DateField()
    start_time = TimeField(**null)
    end_time   = TimeField(**null)
    template   = ForeignKey(EventTemplate, related_name='events', **null)
    calendar   = ForeignKey(Calendar, related_name='events', **null)

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return "%s (%s)" % (self.name, str(self.template))

    def get_absolute_url(self):
        return reverse('diary:event', kwargs={'pk': self.pk})

    @property
    def parent(self):
        d = self.date
        return DayCalendar(day=d.day, month=d.month, year=d.year,
                           calendar=self.calendar.slug)

    class Meta:
        ordering = ('-date',)


class Task(Model):
    """Something that is needed for the event to happen"""
    name  = CharField(max_length=64, default='attend event')
    notes = TextField(**null)
    event = ForeignKey(Event, related_name='tasks')
    owner = ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks')

    def __str__(self):
        return self.name


class Alert(Model):
    """When a user should be alerted that a task is due"""
    task  = ForeignKey(Task)
    user  = ForeignKey(settings.AUTH_USER_MODEL)

    days_before  = IntegerField(default=0)
    hours_before = IntegerField(default=0)

    def __str__(self):
        return "Alert for %s (for user %s)" % (str(self.event or self.task), str(self.user))


# ---=== CMSPlugins Below this line ===--- #

from cms.models import CMSPlugin

class CmsMonthView(CMSPlugin):
    offset = IntegerField(_('Number of months from this month.'), default=0)
    calendar = ForeignKey(Calendar, **null)

    @property
    def month_calendar(self):
        (year, month) = ym(today().year, today().month + self.offset)
        return MonthCalendar(add_events=True, year=year, month=month, **dict(self.kwargs))

    @property
    def kwargs(self):
        if self.calendar:
            yield ('calendar', self.calendar.slug)

