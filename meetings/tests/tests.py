from django.core.urlresolvers import reverse

import datetime

from meetings.models import *
from meetings.forms import *
from person.userextra import User
from .basetest import UserTestCase, StaffTestCase, AdminTestCase

class PermissionsTests(UserTestCase):
    
    def test_create_view_permissions(self):
        """the create view should only be accessible to users with the proper permissions"""
        response = self.client.get(reverse('meetings:create'))
        self.assertNotEqual(response.status_code, 200)

    def test_create_person_view_permissions(self):
        """the create person view should only be accessible to users with the proper permissions"""
        response = self.client.get(reverse('meetings:create_person'))
        self.assertNotEqual(response.status_code, 200)

    def test_edit_view_permissions(self):
        """the edit view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:edit', args=[meeting.pk]))
        self.assertNotEqual(response.status_code, 200)

    def test_prepare_view_permissions(self):
        """the prepare view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:prepare', args=[meeting.pk]))
        self.assertNotEqual(response.status_code, 200)

    def test_proceedings_view_permissions(self):
        """the proceedings view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:proceedings', args=[meeting.pk]))
        self.assertNotEqual(response.status_code, 200)
        
    def test_reedit_view_permissions(self):
        """the reedit view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:re-edit', args=[meeting.pk]))
        self.assertNotEqual(response.status_code, 200)

    def test_delete_meeting_view_permissions(self):
        """the reedit view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:delete_meeting', args=[meeting.pk]))
        self.assertNotEqual(response.status_code, 200)

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

    def test_edit_view_post(self):
        """the edit view should save any changes upon a correctly formatted POST request"""
        meetingDate = datetime.now()
        meeting = Meeting.objects.create(meeting_date=meetingDate, name='meeting', meeting_type=Type.objects.create(name='Type'))
        newType = Type.objects.create(name="Newtype")
        request = self.client.post(reverse('meetings:edit', args=[meeting.pk]), data={'name': 'new_name', 'meeting_date': '5/6/07', 'meeting_type': '2'})
        self.assertEqual(request.status_code, 302)
        meeting = Meeting.objects.get(name='new_name')
        self.assertEqual(meeting.name, 'new_name')
        self.assertEqual(meeting.meeting_date, date(year=2007, month=5, day=6))
        self.assertEqual(meeting.meeting_type, newType)

class MeetingDetailTests(UserTestCase):

    def test_detail_view_template(self):
        """the detail view should render using the proper template"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:detail', args=[meeting.pk]))
        self.assertTemplateUsed(response, 'meetings/meeting_detail.html')
        self.assertEqual(response.status_code, 200)

class MeetingCreateTests(AdminTestCase):
    def test_create_view_template(self):
        """the create view should render using the proper template"""
        response = self.client.get(reverse('meetings:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetings/meeting_create_form.html')

    def test_create_view_post(self):
        """the create view should save any changes upon a correctly formatted POST request"""
        meetingType = Type.objects.create(name='Type')
        self.client.post(reverse('meetings:create'), data={'name': 'meeting', 'meeting_date': '5/6/07', 'meeting_type': '1'})
        meeting = Meeting.objects.get(name='meeting')
        self.assertEqual(meeting.name, 'meeting')
        self.assertEqual(meeting.meeting_date, date(year=2007, month=5, day=6))
        self.assertEqual(meeting.meeting_type, meetingType)

class MeetingProceedingsTests(AdminTestCase):
    def test_proceedings_view_template(self):
        """the proceedings view should render using the proper template"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:proceedings', args=[meeting.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetings/add_meeting_notes.html')

    def test_proceedings_view_post(self):
        """the proceedings view should save any changes upon a correctly formatted POST request"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='meeting', meeting_type=Type.objects.create(name='Type'))
        bill = Person.objects.create(auser=User.objects.create(username="bill", password="123"))
        bipp = Person.objects.create(auser=User.objects.create(username="bipp", password="123"))
        biff = Person.objects.create(auser=User.objects.create(username="biff", password="123"))
        #I don't know why this isn't working =(
        self.client.post(reverse('meetings:proceedings', args=[meeting.pk]), data={'people_late': (1,2,3) })
        self.assertEqual(meeting.people_late.all(),  {bill, bipp, biff})

class MeetingReeditTests(AdminTestCase):
    def test_reedit_view_template(self):
        """the reedit view should render using the proper template"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:re-edit', args=[meeting.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetings/meeting_reedit_form.html')
