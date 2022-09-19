from django import forms

from scrap.forms import widgets as sc_widgets


class ComplicatedModelChoiceField(forms.ModelChoiceField):
    """
    Use a dict instead of a string for its label. The 'label' key is expected
    for the actual label, any other keys will be used as HTML attributes on
    the option.
    """
    additional_fields_for_options = []
    widget = sc_widgets.ComplicatedSelect

    def __init__(self, *args, additional_fields_for_options=None, **kwargs):
        super(ComplicatedModelChoiceField, self).__init__(*args, **kwargs)
        self.additional_fields_for_options = additional_fields_for_options or []

    def label_from_instance(self, obj):
        complicated_label = {'label': str(obj)}
        for additional_field in self.additional_fields_for_options:
            if additional_field == 'label':
                continue
            complicated_label[additional_field] = getattr(obj, additional_field)
        return complicated_label
