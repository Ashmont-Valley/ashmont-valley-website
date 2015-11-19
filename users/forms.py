
from django.forms import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import admin
from django.db.models import ManyToOneRel

from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField

from .models import Person, Address, Building, Road, City, State, Country

class PasswordForm(PasswordResetForm):
    recaptcha = ReCaptchaField(label=_("Human Test"))

class RegisForm(RegistrationForm):
    recaptcha = ReCaptchaField(label=_("Human Test"))

class UserForm(ModelForm):
    password1 = CharField(label=_('Password'), widget=PasswordInput(), required=False)
    password2 = CharField(label=_('Confirm'), widget=PasswordInput(), required=False)

    class Meta:
        model = Person
        exclude = ('user_permissions', 'is_superuser', 'groups', 'last_login',
                   'is_staff', 'is_active', 'date_joined')
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords don't match")
            self.cleaned_data['password'] = password1
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        user = Person.objects.filter(username=username)
        if user and user[0] != self.instance:
            raise ValidationError('Username already taken')
        return username

    def save(self, **kwargs):
        password = self.cleaned_data.get('password', None)
        if password:
            self.instance.set_password(password)
        return ModelForm.save(self, **kwargs)

class PersonForm(UserForm):
    class Meta:
        model = Person
        exclude = ('last_seen','visits','notes', 'created', 'user_permissions', 'is_superuser', 'groups', 'last_login', 'is_staff', 'is_active', 'date_joined', 'password')


class AddressForm(ModelForm):
    number   = CharField()
    name     = CharField(required=False, label="Building Name")
    road     = CharField()
    city     = ModelChoiceField(City.objects.all())
    postcode = CharField()

    class Meta:
        model = Address
        exclude = ('building',)
        folds = ('building.number', 'building.name', 'building.road',
                 'building.road.city', 'building.postcode')

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = {}
        for k in self.Meta.folds:
            if 'instance' in kwargs and kwargs['instance']:
                obj = kwargs['instance']
                for field in k.split('.'):
                    obj = getattr(obj, field)
                kwargs['initial'][field] = obj 
        super(AddressForm, self).__init__(*args, **kwargs)
        add_related_field_wrapper(self, 'city', Road)

    def save(self, commit=True):
        if True:
            building = getattr(self.instance, 'building', None)
            road = getattr(building, 'road', None)
            road = Road.objects.create_or_update(road,
                    name=self.cleaned_data['road'],
                    city=self.cleaned_data['city'])
            building = Building.objects.create_or_update(building, road=road,
                    name=self.cleaned_data['name'],
                    postcode=self.cleaned_data['postcode'],
                    number=self.cleaned_data['number'])
            obj = super(AddressForm, self).save(commit=False)
            obj.building = building
            obj.save()
            return obj
        return super(AddressForm, self).save(commit=False)

def add_related_field_wrapper(form, col_name, model=None):
    rel_model = model or form.Meta.model
    rel = rel_model._meta.get_field(col_name).rel
    form.fields[col_name].widget = RelatedFieldWidgetWrapper(
        form.fields[col_name].widget, rel,
        admin.site, can_add_related=True)


