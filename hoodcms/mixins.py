from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

class AccessMixin(object):
    permissions = []
    login_url = settings.LOGIN_URL
    raise_exception = False # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_login_url(self):
        if self.login_url is None:
            raise ImproperlyConfigured("%(cls)s is missing the login_url. "
                "Define %(cls)s.login_url or override "
                "%(cls)s.get_login_url()." % {"cls": self.__class__.__name__})
        return self.login_url

    def get_redirect_field_name(self):
        if self.redirect_field_name is None:
            raise ImproperlyConfigured("%(cls)s is missing the "
                "redirect_field_name. Define %(cls)s.redirect_field_name or "
                "override %(cls)s.get_redirect_field_name()." % {
                "cls": self.__class__.__name__})
        return self.redirect_field_name

    def is_authorised(self, user):
        for p in self.permissions:
            if not user.has_perm(p):
                return False
        return True

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated() or not self.is_authorised(user):
            if self.raise_exception:
                raise PermissionDenied # return a forbidden response
            else:
                return redirect_to_login(request.get_full_path(),
                    self.get_login_url(), self.get_redirect_field_name())
        return super(AccessMixin, self).dispatch(request, *args,
            **kwargs)



