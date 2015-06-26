from django.core.urlresolvers import reverse

import datetime

from meetings.models import *
from .basetest import UserTestCase, StaffTestCase, AdminTestCase

class MeetingIndexTests(AdminTestCase):

    def test_index_view_template(self):
        """the index view should render using the proper template"""
        response = self.client.get(reverse('meetings:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetings/meeting_list.html')

    def test_meeting_index_view_with_future_meeting(self):
        """the meeting index should have links to the meeting edit, detail, and create pages if its meeting_date is in the future and it has no start time"""
        date = datetime.now() + timedelta(days=4)
        meeting = Meeting.objects.create(meeting_date=date, name='Future', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:index'))
        self.assertContains(response, 'href="%s"' % reverse('meetings:detail', args=[meeting.pk]))
        self.assertContains(response, 'href="%s"' % reverse('meetings:edit', args=[meeting.pk]))
        self.assertContains(response, 'href="%s"' % reverse('meetings:create'))

    def test_meeting_index_view_with_meeting_today(self):
        """the meeting index should have links to the meeting prepare, detail, and create pages if its meeting_date is today and it has no start time"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Today', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:index'))
        self.assertContains(response, 'href="%s"' % reverse('meetings:detail', args=[meeting.pk]))
        self.assertContains(response, 'href="%s"' % reverse('meetings:prepare', args=[meeting.pk]))
        self.assertContains(response, 'href="%s"' % reverse('meetings:create'))

    def test_meeting_index_view_with_ongoing_meeting(self):
        """the meeting index should have links to the meeting proceedings, detail, and create pages if its meeting_date is today and it has a start time"""
        date = datetime.now()
        time = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Ongoing', meeting_type=Type.objects.create(name='Type'), start_time=time)
        response = self.client.get(reverse('meetings:index'))
        self.assertContains(response, 'href="%s"' % reverse('meetings:detail', args=[meeting.pk]))
        self.assertContains(response, 'href="%s"' % reverse('meetings:proceedings', args=[meeting.pk]))
        self.assertContains(response, 'href="%s"' % reverse('meetings:create'))

    def test_meeting_index_view_with_ongoing_meeting(self):
        """the meeting index should have links to the meeting re-edit, detail, and create pages if its meeting_date is today and it has an endtime"""
        date = datetime.now()
        time = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Ongoing', meeting_type=Type.objects.create(name='Type'), end_time=time)
        response = self.client.get(reverse('meetings:index'))
        self.assertContains(response, 'href="%s"' % reverse('meetings:detail', args=[meeting.pk]))
        self.assertContains(response, 'href="%s"' % reverse('meetings:re-edit', args=[meeting.pk]))
        self.assertContains(response, 'href="%s"' % reverse('meetings:create'))

class MeetingEditTests(AdminTestCase):

    def test_edit_view_template(self):
        """the edit view should render using the proper template"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:edit', args=[meeting.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetings/meeting_edit_form.html')

class MeetingDetailTests(UserTestCase):

    def test_detail_view_template(self):
        """the detail view should render using the proper template"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:detail', args=[meeting.pk]))
        self.assertTemplateUsed(response, 'meetings/meeting_detail.html')
        self.assertEqual(response.status_code, 200)

class MeetingCreateTests(UserTestCase):
    def test_create_view_template(self):
        """the create view should render using the proper template"""
        response = self.client.get(reverse('meetings:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetings/meeting_create_form.html')

