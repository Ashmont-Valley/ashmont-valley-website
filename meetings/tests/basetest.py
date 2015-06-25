import os

from django.test import TestCase
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse

class UserTestCase(TestCase):
    """For users"""

    fixtures = ['test-auth']

    def setUp(self):
        self.client.login(username='admin', password='123456')
        self.client.session.save()

