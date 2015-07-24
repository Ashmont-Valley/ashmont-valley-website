from django.core.urlresolvers import reverse

import datetime

from meetings.models import *
from meetings.forms import *
from person.userextra import User
from django.utils.text import slugify
from .basetest import UserTestCase, StaffTestCase, AdminTestCase

class PermissionsTests(UserTestCase):
    def test_create_view_permissions(self):
        """the create view should only be accessible to users with the proper permissions"""
        response = self.client.get(reverse('meetings:create'))
        self.assertEqual(response.status_code, 302)

    def test_create_person_view_permissions(self):
        """the create person view should only be accessible to users with the proper permissions"""
        response = self.client.get(reverse('meetings:create_person'))
        self.assertEqual(response.status_code, 302)

    def test_edit_view_permissions(self):
        """the edit view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:edit', args=[meeting.pk]))
        self.assertEqual(response.status_code, 302)

    def test_prepare_view_permissions(self):
        """the prepare view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:prepare', args=[meeting.pk]))
        self.assertEqual(response.status_code, 302)

    def test_proceedings_view_permissions(self):
        """the proceedings view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:proceedings', args=[meeting.pk]))
        self.assertEqual(response.status_code, 302)
        
    def test_reedit_view_permissions(self):
        """the reedit view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:re-edit', args=[meeting.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_meeting_view_permissions(self):
        """the delete view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:delete_meeting', args=[meeting.pk]))
        self.assertEqual(response.status_code, 302)

    def test_create_person_view_permissions(self):
        """the create person view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:create_person'))
        self.assertEqual(response.status_code, 302)

    def test_add_note_view_permissions(self):
        """the add note view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:add_note', args=[meeting.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_note_view_permissions(self):
        """the delete note view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        note = Note.objects.create(meeting=meeting, text="note")
        response = self.client.get(reverse('meetings:delete_note', args=[note.pk]))
        self.assertEqual(response.status_code, 302)

    def test_update_note_view_permissions(self):
        """the update note view should only be accessible to users with the proper permissions"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        note = Note.objects.create(meeting=meeting, text="note")
        response = self.client.get(reverse('meetings:update_note', args=[note.pk]))
        self.assertEqual(response.status_code, 302)

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
        bill = Person.objects.create(user=User.objects.create(username="bill", password="123"))
        bipp = Person.objects.create(user=User.objects.create(username="bipp", password="123"))
        biff = Person.objects.create(user=User.objects.create(username="biff", password="123"))
        self.client.post(reverse('meetings:proceedings', args=[meeting.pk]), data={'people_late__in': (bill.pk, bipp.pk, biff.pk) })
        self.assertEqual(list(meeting.people_late.all()),  {bill, bipp, biff})

class MeetingReeditTests(AdminTestCase):
    def test_reedit_view_template(self):
        """the reedit view should render using the proper template"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), end_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:re-edit', args=[meeting.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetings/meeting_reedit_form.html')

class MeetingCreatePersonTests(AdminTestCase):
    def test_create_person_view_post_first_name_only(self):
        """the create person view should create a person and attached user upon a correctly formatted POST request"""
        name = 'Jon'
        response = self.client.post(reverse('meetings:create_person'), data={'first_name': name})
        self.assertEqual(response.data['name'], name)
        person = Person.objects.get(pk=response.data['pk'])
        user = person.user
        self.assertEqual(user.first_name, name)
        self.assertEqual(user.username, name)
        self.assertEqual(user.last_name, None)

    def test_create_person_view_post_first_and_last_name(self):
        """the create person view should create a person and attached user upon a correctly formatted POST request"""
        name = 'Jon Smith'
        response = self.client.post(reverse('meetings:create_person'), data={'first_name': name})
        self.assertEqual(response.data['name'], name)
        person = Person.objects.get(pk=response.data['pk'])
        user = person.user
        self.assertEqual(user.first_name, 'Jon')
        self.assertEqual(user.username, slugify(name))
        self.assertEqual(user.last_name, 'Smith')

    def test_create_person_view_post_with_more_than_two_names(self):
        """the create person view should create a person and attached user upon a correctly formatted POST request"""
        name = 'Jon Leeroy Jenkins Smith'
        response = self.client.post(reverse('meetings:create_person'), data={'first_name': name})
        self.assertEqual(response.data['name'], name)
        person = Person.objects.get(pk=response.data['pk'])
        user = person.user
        self.assertEqual(user.first_name, 'Jon Leeroy Jenkins')
        self.assertEqual(user.username, slugify(name))
        self.assertEqual(user.last_name, 'Smith')

    def test_create_person_view_post_duplicate_people(self):
        """the create person view should create a person and a user if they do not already exist"""
        name = 'Jon Smith'
        self.assertEqual(Person.objects.count(first_name='Jon', last_name='Smith'), 0)
        self.client.post(reverse('meetings:create_person'), data={'first_name': name})
        self.assertEqual(Person.objects.count(first_name='Jon', last_name='Smith'), 1)
        self.client.post(reverse('meetings:create_person'), data={'first_name': name})
        self.assertEqual(Person.objects.count(first_name='Jon', last_name='Smith'), 1)

class MeetingDeleteViewTests(AdminTestCase):
    def test_meeting_delete_view(self):
        """the meeting delete view should delete meetings upon a POST request"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', meeting_type=Type.objects.create(name='Type'))
        #need to check if in database
        self.client.post(reverse('meetings:delete', args=[meeting.pk]))
        #need to check if not in database

    def test_meeting_delete_view(self):
        """the meeting delete view should only delete meetings that haven't begun yet"""
        date = datetime.now()
        meeting = Meeting.objects.create(meeting_date=date, name='Meeting', start_time=date.time(), meeting_type=Type.objects.create(name='Type'))
        #need to check if in database
        self.client.post(reverse('meetings:delete', args=[meeting.pk]))
        #need to check if still in database
