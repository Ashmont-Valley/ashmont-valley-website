
from datetime import timedelta
from django.db.models import *
from django.utils.text import slugify

from django.core.urlresolvers import reverse
from django.conf import settings

class Calendar(Model):
    """A collection of events for a specific calendar"""
    name   = CharField(max_length=32)
    slug   = SlugField(max_length=32, blank=True)
    owner  = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    public = BooleanField(default=True)

    # If events are sourced from somewhere else, then we need the url
    # where we can find those events (must be http).
    import_src = URLField(null=True, blank=True)

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
    desc       = TextField(null=True, blank=True)
    start_time = TimeField(null=True, blank=True)
    end_time   = TimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class TaskTemplate(Model):
    """A task that needs to be done every time the event is created"""
    name       = CharField(max_length=64, default='attend event')
    notes      = TextField(null=True, blank=True)
    template   = ForeignKey(EventTemplate, related_name='tasks')

    def __str__(self):
        return self.name


class EventQuerySet(QuerySet):
    __str__ = lambda self: "Events"

    def get_absolute_url(self):
        return reverse('diary:index')


class Event(Model):
    """Something that will happen on a specific date/time"""
    date       = DateField()
    start_time = TimeField(null=True, blank=True)
    end_time   = TimeField(null=True, blank=True)
    template   = ForeignKey(EventTemplate, related_name='events')
    calendar   = ForeignKey(Calendar, related_name='events', null=True, blank=True)

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
    notes = TextField(null=True, blank=True)
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



