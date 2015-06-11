from django.core.urlresolvers import reverse
import datetime

from django.test import TestCase

from meetings.models import *

class MeetingIndexToDetailOrEditTests(TestCase):
    def test_meeting_index_view_with_future_meeting(self):
        """the meeting index view should link to the meeting detail page if it's
        meeting_date is in the future"""
        time = datetime.datetime.now() + datetime.timedelta(days=1)
        future_meeting = Meeting.objects.create(meeting_date=time, 
            name='Future', meeting_type=Type.objects.create(name='Type'))
        #how do you do this?

class MeetingEditTests(TestCase):
    def test_edit_view_with_future_meeting(self):
        """the edit view of a future meeting should return a 404 error"""
        time = datetime.datetime.now() + datetime.timedelta(days=1)
        future_meeting = Meeting.objects.create(meeting_date=time, 
            name='Future', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:meeting_edit', 
            args=(future_meeting.pk)))
        self.assertEqual(response.status_code, 404)

    def test_edit_view_with_meeting_less_than_a_week_ago(self):
        """the edit view of a meeting that happened less than a week ago
        should display the edit form"""
        time = datetime.datetime.now() - datetime.timedelta(days=3)
        future_meeting = Meeting.objects.create(meeting_date=time, 
            name='<week', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:meeting_edit',
            args=(future_meeting.pk)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meeting_edit_form.html') 
                
    def test_edit_view_with_meeting_more_than_a_week_ago(self):
        """the edit view of a meeting that took place more than a week ago
         should return a 404 error"""
        time = datetime.datetime.now() - datetime.timedelta(days=8)
        future_meeting = Meeting.objects.create(meeting_date=time, 
            name='>week', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:meeting_edit',
            args=(future_meeting.pk)))
        self.assertEqual(response.status_code, 404)


class MeetingDetailTests(TestCase):
    def test_detail_view_with_meeting_more_than_a_week_ago(self):
        """the detail view of a meeting that happened more than a week ago
        should display the details of the meeting"""
        time = datetime.datetime.now() - datetime.timedelta(days=8)
        future_meeting = Meeting.objects.create(meeting_date=time,
            name='>week', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:meeting_detail',
            args=(future_meeting.pk)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meeting_detail.html')

    def test_detail_view_with_future_meeting(self):
        """the detail view of a future meeting should display the 
        details of the meeting"""
        time = datetime.datetime.now() + datetime.timedelta(days=1)
        future_meeting = Meeting.objects.create(meeting_date=time,
            name='future', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(reverse('meetings:meeting_detail',
            args=(future_meeting.pk)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meeting_detail.html')

    #what should detailview for the past week show?

class MeetingCreateTests:
    def test_create_view_template(self):
        """the create view should render using the proper template"""
        response = self.client.get(reverse('meetings:meeting_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meeting_create_form.html')
