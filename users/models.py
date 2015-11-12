
import os

from django.db.models import *


from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator

from django.contrib.auth.models import AbstractUser, Group
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils.timezone import now
from django.conf import settings

from geoposition.fields import GeopositionField

null = dict(null=True, blank=True)

from hoodcms.fields import ResizedImageField

@python_2_unicode_compatible
class ContactType(Model):
    name    = CharField(max_length=16)
    icon    = CharField(max_length=32)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Person(AbstractUser):
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

    @property
    def name(self):
        """Adds the first and last name as a full name or username"""
        if self.first_name or self.last_name:
            return self.get_full_name()
        return self.username

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_profile', kwargs={'username':self.username})

    def visited_by(self, by_user):
        if by_user != self:
            self.visits += 1
            self.save()


# ===== Friendships ===== #

#class FriendshipManager(Manager):
#    def i_added(self):
#        from cms.utils.permissions import get_current_user as get_user
#        user = get_user()
#        if user.is_authenticated():
#            return bool(self.get(from_user=user.pk))
#        return False

#class Friendship(Model):
#    from_user = ForeignKey(Person, related_name='friends')
#    user = ForeignKey(Person, related_name='from_friends')
#    objects = FriendshipManager()


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

