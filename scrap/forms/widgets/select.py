from django.forms import widgets


class ComplicatedSelect(widgets.Select):
    """
    Use a dict instead of a string for its label. The 'label' key is expected
    for the actual label, any other keys will be used as HTML attributes on
    the option.
    """
    # option_template_name = "scrap/forms/widgets/select_option.html"

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        # This allows using strings labels as usual
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop('label')
        else:
            opt_attrs = {}
        option_dict = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        for key, val in opt_attrs.items():
            option_dict['attrs'][key] = val
        return option_dict
