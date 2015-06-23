
from django.utils.text import slugify
from django.views.generic.list import MultipleObjectMixin, ListView

class MultiListView(ListView):
    def get_querysets(self):
        return [
          (None, self.get_queryset())
        ]

    def get_context_data(self, **kwargs):
        data = self.get_querysets()
        context = {
          'lists': list(self.generate_lists(data)),
          'names': [ (slugify(unicode(i)), str(i)) for (i, j) in data ],
        }
        return super(MultipleObjectMixin, self).get_context_data(**context)
        
    def generate_lists(self, data):
        for (name, qs) in data:
            src = super(MultiListView, self).get_context_data(object_list=qs)
            yield [
                slugify(unicode(name)),
                src['object_list'], src['paginator'],
                src['page_obj'], src['is_paginated'],
              ]

