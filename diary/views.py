
from django.utils.translation import ugettext_lazy as _
from django.views.generic import *
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Calendar, Event
from .mixins import AccessMixin, GeneratedObjectView
from .generated import DayCalendar, MonthCalendar, YearCalendar

class DailyCalendar(AccessMixin, GeneratedObjectView):
    model = DayCalendar

class MonthlyCalendar(AccessMixin, GeneratedObjectView):
    model = MonthCalendar

class MonthlyMiniCalendar(AccessMixin, GeneratedObjectView):
    model = MonthCalendar
    template_name = 'diary/includes/month.html'

class YearlyCalendar(AccessMixin, GeneratedObjectView):
    model = YearCalendar

class FullCalendar(AccessMixin, DetailView):
    slug_url_kwarg = 'calendar'
    action_name = None
    model = Calendar

class AllEvents(AccessMixin, ListView):
    action_name = None
    model = Event

    def listing(request):
        event_list = Event.objects.all()
        paginator = Paginator(event_list, 3)

        page = request.GET.get('page')
        try:
            event = paginator.page(page)
        except PageNotAnInteger:
            event = paginator.page(1)
        except EmptyPage:
            event = page(paginator.num_pages)
        return render_to_response('event_list.html', {"event": event})

class Event(AccessMixin, DetailView):
    model = Event

