import logging

from rest_framework import response, views


logger = logging.getLogger(__name__)


class WideFilterView(views.APIView):
    model = None
    serializer = None
    prefetch_fields = None
    order_fields = None

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, format=None):
        # wide_filter_fields = list of GET keys to look for.  So other args can be used and not get in the way.
        # /inventory/api_rawitem/wide_filter/?wide_filter_fields=name&name=beef+ground&empty=false
        # /inventory/api_rawitem/wide_filter/?wide_filter_fields[]=name&name=beef+ground&empty=false
        if (request.GET.get('empty') or 'true') == 'true':
            # Shortcut an empty filter request.  We could send back a sample set, all, or none.
            return response.Response(self.serializer(self.get_queryset().none(), many=True).data)
        data = self.serializer(self.filter_qs(self.request_params_to_search_terms(request)), many=True).data
        return response.Response(data)

    def filter_qs(self, search_terms):
        filter_qs = self.model.objects.wide_filter(search_terms)
        qs = self.get_queryset().filter(id__in=filter_qs)
        qs = self.order_qs(self.prefetch_qs(qs))
        return qs

    def order_qs(self, qs):
        if self.order_fields:
            return qs.order_by().order_by(*self.order_fields)

    def prefetch_qs(self, qs):
        if self.prefetch_fields:
            return qs.prefetch_related(*self.prefetch_fields)
        return qs

    def request_params_to_search_terms(self, request):
        # wide_filter expects
        # search_terms = [
        #     ('name', ('ground', 'beef')),
        #     ('category', 'meats'),
        # ]
        log_prefix = "WideFilterView.request_params_to_search_terms"
        filter_fields = request.GET.getlist('wide_filter_fields[]')
        logger.debug(f"{log_prefix}: filter_fields = {filter_fields}")
        filter_fields_and_values = []
        for filter_field in filter_fields:
            filter_tuple = ()
            if filter_field in request.GET:
                filter_tuple = (filter_field, request.GET.get(filter_field) or '')
            if f"{filter_field}[]" in request.GET:
                # TODO: this doesn't call split.  Does that mean these can include spaces?
                filter_tuple = (filter_field, (request.GET.getlist(f"{filter_field}[]") or []))
            if filter_tuple:
                filter_fields_and_values.append(filter_tuple)
        logger.debug(
            f"{log_prefix}: filter_fields_and_values = {filter_fields_and_values}")
        return filter_fields_and_values
