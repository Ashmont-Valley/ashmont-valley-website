from django.db import models
from datetime import *
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

class Person(models.Model):
    name = models.CharField(help_text=_('the name of the person'), 
        max_length=100, unique=True)
    ordering = ['-name']
    
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Meeting(models.Model):
    name = models.CharField(help_text=_("name of the meeting"), max_length=100)
    meeting_type = models.ForeignKey(Type, help_text=_('type of the meeting'),
        related_name='meetings')

    meeting_date = models.DateField(
        help_text=_('date on which the meeting took place'))
    start_time = models.TimeField(
        help_text=_('time at which the meeting started'), 
        blank=True, null=True)
    end_time = models.TimeField(help_text=_('time at which the meeting ended'), 
        blank=True, null=True)

    people_attending = models.ManyToManyField(Person, 
        related_name='people_attending', 
        help_text=_("list of people who attended the meeting"),
        blank=True, null=True)
    people_absent = models.ManyToManyField(Person, 
        related_name='people_absent',
        help_text=_("list of people who were absent from the meeting"), 
        blank=True, null=True)
    people_guests = models.ManyToManyField(Person, 
        related_name='people_guests',
        help_text=_("list of people who were guests at the meeting"), 
        blank=True, null=True)
    people_late = models.ManyToManyField(Person,
        related_name='people_late',
        help_text=_("list of pople who arrived late at the meeting"),
        blank=True, null=True)
    chair = models.ForeignKey(Person, related_name="chair",
        help_text=_("chair of the meeting"), blank=True, null=True) 
    secretary = models.ForeignKey(Person, related_name='secretary',
        help_text=_("secretary of the meeting"), blank=True, null=True)
    ordering = ['-meeting_date', 'name']

    def is_old(self):
        return self.meeting_date < date.today()

    def is_editable(self):
        """meetings are editable if they have occurred in the past week"""
        time_cutoff = timedelta(days=14) + self.meeting_date
        return (self.meeting_date <= date.today() <= time_cutoff)

    def get_absolute_url(self):
        if self.is_editable() and not self.end_time:
            if self.start_time:
                return reverse('meetings:proceedings', args=[self.pk])
            return reverse('meetings:edit', args=[self.pk])
        return reverse('meetings:detail', args=[self.pk])
        

    def __str__(self):
        return self.name

class Note(models.Model):
    meeting = models.ForeignKey(Meeting, related_name='notes',
        help_text=_("meeting that the note is for"))
    text = models.TextField(help_text=_("text of the note"))
    time_created = models.DateTimeField(
        help_text=_("time at which the note was created"), auto_now_add=True)
    time_edited = models.DateTimeField(
        help_text=_("time at which the note was last edited"), auto_now=True)

    def __str__(self):
        return self.text

