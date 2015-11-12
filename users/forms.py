
from django.forms import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm

from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField

from .models import Person

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

