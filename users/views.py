# -*- coding: utf-8 -*-

from django.views.generic import UpdateView, DetailView, ListView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages

from hoodcms.mixins import LoginRequiredMixin
from .models import Person
from .forms import PersonForm

class UserMixin(LoginRequiredMixin):
    def get_object(self):
        return self.request.user

class EditProfile(UserMixin, UpdateView):
    form_class = PersonForm

    def get_success_url(self):
        return self.get_object().get_absolute_url()

class FacesView(LoginRequiredMixin, ListView):
    template_name = 'users/profiles.html'
    queryset = Person.objects.all()

class ProfileView(DetailView):
    template_name  = 'users/profile.html'
    slug_url_kwarg = 'username'
    slug_field     = 'username'
    model = Person

    def get_object(self, **kwargs):
        user = super(ProfileView, self).get_object(**kwargs)
        user.visited_by(self.request.user)
        return user

class MyProfile(UserMixin, ProfileView):
    pass

# ====== FRIENDSHIP VIEWS =========== #

class MakeFriend(LoginRequiredMixin, SingleObjectMixin, RedirectView):
    slug_url_kwarg = 'username'
    slug_field     = 'username'
    model          = Person

    def get_object(self):
        user = SingleObjectMixin.get_object(self)
        (obj, new) = self.request.user.friends.get_or_create(user=user)
        if new:
            messages.success(self.request, "Friendship created with %s" % str(user))
        else:
            messages.error(self.request, "Already a friend with %s" % str(user))
        return user

    def get_redirect_url(self, **kwargs):
        return self.get_object().get_absolute_url()

class LeaveFriend(MakeFriend):
    def get_object(self):
        user = SingleObjectMixin.get_object(self)
        self.request.user.friends.filter(user=user).delete()
        messages.success(self.request, "Friendship removed from %s" % str(user))
        return user


