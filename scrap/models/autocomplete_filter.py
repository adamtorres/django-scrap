import logging

from django.core import exceptions
from django.db import models

from scrap import utils as sc_utils


logger = logging.getLogger(__name__)


class AutocompleteFilterManagerMixin:
    def autocomplete_filter(self, terms, field, extra_data=None):
        """
        Goal: search the model and return a distinct list of the specified field.
        The search can look in more than just the specified field?
        """
        if isinstance(terms, str):
            terms = terms.split()
        combined_filter = self.model.get_autocomplete_filter(terms, extra_data)
        logger.debug(f"AutocompleteFilterManagerMixin.autocomplete_filter: combined_filter = {combined_filter}")
        qs = self.filter(combined_filter).order_by().distinct('id')
        # Use the above qs as the filter for a clean queryset.  This allows users of the autocomplete_filter to do
        # whatever they want and not have to tiptoe around the distinct clause.
        # Ex:
        # RawItem.objects.autocomplete_filter(['burger', 'bun'], 'cryptic_name').order_by('cryptic_name')
        return self.filter(id__in=qs).order_by().order_by(field).distinct(field)


class AutocompleteFilterModelMixin:
    # autocomplete_filter_fields = ['list', 'of', 'fields', 'to', 'search]
    autocomplete_extra_data_fields = dict()  # key=key from extra_data, value=field on model

    @classmethod
    def get_available_autocomplete_filters(cls):
        if (
                not hasattr(cls, 'autocomplete_filter_fields')
                or not isinstance(getattr(cls, 'autocomplete_filter_fields'), list)):
            raise exceptions.ImproperlyConfigured("wide_filter_fields must be declared on the model.")
        return cls.autocomplete_filter_fields

    @classmethod
    def get_autocomplete_filter(cls, terms, extra_data=None):
        q = models.Q()
        autocomplete_filter_fields = cls.autocomplete_filter_fields
        if isinstance(autocomplete_filter_fields, str):
            autocomplete_filter_fields = [autocomplete_filter_fields]
        for field in autocomplete_filter_fields:
            if isinstance(terms, str):
                terms = terms.split()
            term_q = models.Q()
            for search_term in terms:
                filter_func = "__icontains" if isinstance(search_term, str) else ""
                if field == 'id' or field.endswith('_id'):
                    # UUID doesn't like icontains
                    filter_func = ""
                    if not sc_utils.is_valid_uuid(search_term):
                        # Not a valid uuid so shouldn't be used to filter on uuid fields.
                        continue
                term_q = term_q & models.Q(**{f"{field}{filter_func}": search_term})
            q = q | term_q
        if extra_data and cls.autocomplete_extra_data_fields:
            ed_q = models.Q()
            for ed_field in extra_data.keys():
                if ed_field not in cls.autocomplete_extra_data_fields:
                    logger.error(f"Missing autocomplete_extra_data_fields key '{ed_field}'.  Ignoring it as a result.")
                else:
                    # Currently using this just with uuids so not concerned about icontains or such.
                    ed_q = ed_q & models.Q(**{cls.autocomplete_extra_data_fields[ed_field]: extra_data[ed_field]})
            # Because of the possibility ed_field isn't in autocomplete_extra_data_fields, the ed_q might be empty.
            # But that doesn't make a difference and Django handles the empty Q() just fine.
            q = q & ed_q
        return q
