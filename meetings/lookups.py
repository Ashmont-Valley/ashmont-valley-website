from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from person.models import Person

class PersonLookup(LookupChannel):
    model = Person

    def get_query(self, q, request):
        return Person.objects.filter(Q(auser.name__icontains=q)).order_by('auser.name()')

    def get_result(self, obj):
        return obj.auser.name()

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return u"%s" % escape(obj.auser.name)

    def check_auth(self, request):
        return True

    def can_add(self, user, argmodel):
        return True
