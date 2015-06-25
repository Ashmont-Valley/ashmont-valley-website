from django.core.urlresolvers import reverse
import datetime

from django.test import TestCase, Client

from meetings.models import *

class MeetingIndexTests(TestCase):

    def test_index_view_template(self):
        """the index view should render using the proper template"""
        response = self.client.get(reverse('meetings:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meeting_list.html')

    def test_meeting_index_view_with_future_meeting(self):
        """the meeting index should have links to the meeting edit, detail, and create pages if it's meeting_date is in the future"""
        date = datetime.now() + timedelta(days=4)
        meeting = Meeting.objects.create(meeting_date=date, name='Future', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:index'))
        self.assertContains(response, 'href=' + reverse('meetings:detail', args=[meeting.pk]), html=True)
        self.assertContains(response, 'href=' + reverse('meetings:edit', args=[meeting.pk]), html=True)
        self.assertContains(response, 'href=' + reverse('meetings:create'), html=True)

class MeetingEditTests(TestCase):

    def test_edit_view_template(self):
        """the edit view should render using the proper template"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:edit', args=[meeting.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meeting_edit_form.html')

class MeetingDetailTests(TestCase):

    def test_detail_view_template(self):
        """the detail view should render using the proper template"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:detail', args=[meeting.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meeting_detail.html')

class MeetingCreateTests:
    def test_create_view_template(self):
        """the create view should render using the proper template"""
        response = self.client.get(reverse('meetings:meeting_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meeting_create_form.html')
