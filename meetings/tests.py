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
        response = self.client.get(


                )


class MeetingEditTests(TestCase):
    def test_edit_view_with_future_meeting(self):
        """the edit view of a future meeting should return a 404 error"""
        time = datetime.datetime.now() + datetime.timedelta(days=1)
        future_meeting = Meeting.objects.create(meeting_date=time, 
            name='Future', meeting_type=Type.objects.create(name='Type'))
        response = self.client.get(


