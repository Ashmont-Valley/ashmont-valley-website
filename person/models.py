
import os

from django.db.models import *


from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator

from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils.timezone import now
from django.conf import settings

from geoposition.fields import GeopositionField

null = dict(null=True, blank=True)

from .fields import ResizedImageField, AutoOneToOneField
from .userextra import User, Group

class ContactType(Model):
    name    = CharField(max_length=16)

    def __unicode__(self):
        return self.name


class Person(Model):
    user  = AutoOneToOneField(User, related_name='details', unique=True)

    photo = ResizedImageField(_('Photograph (square)'), null=True, blank=True,
              upload_to='photos', max_width=190, max_height=190)

    notes   = TextField(**null)
    phone   = CharField(_('Cell Phone'), max_length=8, **null)

    ctype   = ForeignKey(ContactType, verbose_name=_('Contact Type'), **null)
    org     = CharField(_('Organization'), max_length=64, **null)
    ophone  = CharField(_('Office Phone'), max_length=32, **null)
    desc    = CharField(_('Description'), max_length=255, **null)

    created   = DateTimeField(default=now)
    last_seen = DateTimeField(**null)
    visits    = IntegerField(default=0)

    def __unicode__(self):
        return self.name()

    def __str__(self):
        return unicode(self)

    def get_absolute_url(self):
        return self.user.get_absolute_url()

    @property
    def first_name(self):
        if self.user.first_name:
            return self.user.first_name
        return None

    @property
    def last_name(self):
        if self.user.last_name:
            return self.user.last_name
        return None

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None

    def name(self):
        return self.user.name()


class Twilight(Manager):
    def i_added(self):
        from cms.utils.permissions import get_current_user as get_user
        user = get_user()
        if user.is_authenticated():
            return bool(self.get(from_user=user.pk))
        return False

class Friendship(Model):
    from_user = ForeignKey(User, related_name='friends')
    user = ForeignKey(User, related_name='from_friends')
    objects = Twilight()

# ===== Addresses ===== #

class Country(Model):
    name     = CharField(max_length=128)
    code     = CharField(max_length=2)
    
    def __unicode__(self):
        return self.name

class State(Model):
    name     = CharField(max_length=128)
    code     = CharField(max_length=2)
    country  = ForeignKey(Country)
    
    def __unicode__(self):
        return self.name

class City(Model):
    name     = CharField(max_length=128)
    state    = ForeignKey(State)

    def __unicode__(self):
        return self.name

class Road(Model):
    name     = CharField(max_length=128)
    alias    = CharField(max_length=128, **null)
    city     = ForeignKey(City)

    def __unicode__(self):
        return self.name

class Building(Model):
    """Provides a way to specify the co-ords for a plot/address"""
    number   = CharField(max_length=6)
    name     = CharField(max_length=64)

    road     = ForeignKey(Road)    
    postcode = CharField(max_length=22)
    location = GeopositionField(**null)

    plot     = TextField(_('Building Plot'), **null)
    foot     = TextField(_('Building Footprint'), **null)

    class Meta:
        unique_together = (('number', 'road'),)

    def coords(self, c_latt, c_long):
        if self.location:
            return (
                coord(self.location.latitude, *c_latt),
                coord(self.location.longitude, *c_long),
            )
        return None

    def __unicode__(self, extra=''):
        return "%s %s%s\n%s\n%s" % (self.number, self.road, extra, self.road.city, self.road.city.state)

class Address(Model):
    """An address is some relatable information plus a building"""
    TYPES = (
      ('-', 'Unknown'),
      ('R', 'Residence'),
      ('B', 'Business'),
      ('C', 'Community Space'),
      ('G', 'Governmental'),
    )

    building  = ForeignKey(Building)
    apt       = CharField(max_length=32, **null)
    phone     = CharField(_('Adress Phone'), max_length=32, **null)
    kind      = CharField(_('Type'), max_length=1, choices=TYPES, default='-')
    importid  = CharField(_('Whitepages ID'), max_length=128, **null)

    class Meta:
        unique_together = (('apt', 'building'),)

    def __unicode__(self):
        if self.apt:
            return self.building.__unicode__(', (Apt %s)' % self.apt)
        return unicode(self.building)


# ===== CMS Plugins ===== #


from cms.models import CMSPlugin

class GroupPhotoPlugin(CMSPlugin):
    STYLES = (
      ('L', _('Simple List')),
      ('P', _('Photo Heads')),
      ('B', _('Photo Bios')),
    )

    source = ForeignKey(Group)
    style  = CharField(_('Display Style'), max_length=1, choices=STYLES)


