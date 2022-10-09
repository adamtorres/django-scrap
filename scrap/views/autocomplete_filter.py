import logging

from rest_framework import response, views


logger = logging.getLogger(__name__)


class AutocompleteFilterView(views.APIView):
    model = None
    serializer = None
    prefetch_fields = None

    def distinct_qs(self, qs, field):
        return qs.distinct().distinct(field)

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, format=None):
        terms = request.GET.get('terms')
        field = request.GET.get('field')
        if not terms or not field:
            return response.Response(self.serializer(self.get_queryset().none(), many=True).data)
        qs = self.filter_qs(terms, field)
        data = self.serializer(qs, many=True).data
        return response.Response(data)

    def filter_qs(self, terms, field):
        filter_qs = self.model.objects.autocomplete_filter(terms, field)
        qs = self.get_queryset().filter(id__in=filter_qs)
        qs = self.prefetch_qs(qs)
        qs = self.distinct_qs(self.order_qs(qs, field), field)
        return qs

    def order_qs(self, qs, field):
        return qs.order_by().order_by(field)

    def prefetch_qs(self, qs):
        if self.prefetch_fields:
            return qs.prefetch_related(*self.prefetch_fields)
        return qs
