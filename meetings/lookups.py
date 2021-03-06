from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from users.models import Person

class PersonLookup(LookupChannel):
    model = Person

    def get_query(self, q, request):
        return Person.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q)).order_by('last_name', 'first_name')

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return u"%s" % escape(obj.name)

    def check_auth(self, request):
        return True

    def can_add(self, user, argmodel):
        return True
