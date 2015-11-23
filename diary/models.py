
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta
from django.db.models import *
from django.utils.text import slugify

from django.core.urlresolvers import reverse
from django.conf import settings

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

    @property
    def parent(self):
        return Event.objects.all()

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Calendar, self).save(**kwargs)


class EventTemplate(Model):
    """A description of an event with some default tasks""" 
    name       = CharField(max_length=64)
    desc       = TextField(**null)
    start_time = TimeField(**null)
    end_time   = TimeField(**null)

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
        return str(self.template)

    def get_absolute_url(self):
        return reverse('diary:event', kwargs={'pk': self.pk})

    @property
    def parent(self):
        from diary.generated import DayCalendar
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
        from .generated import ym, today, MonthCalendar
        (year, month) = ym(today().year, today().month + self.offset)
        cal = MonthCalendar(year=year, month=month, **dict(self.kwargs))
        list(cal)
        return cal

    @property
    def kwargs(self):
        if self.calendar:
            yield ('calendar', self.calendar.slug)

