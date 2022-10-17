from django import forms


class AutocompleteWidget(forms.widgets.TextInput):
    template_name = "scrap/forms/widgets/autocomplete.html"
    placeholder = "needs a value"

    class Media:
        css = {
            'all': ('3rdparty/bootstrap-5.1.3-dist/css/bootstrap.css', 'css/autocomplete.css', )
        }
        js = [
            '3rdparty/js/jquery-3.6.0.min.js',
            '3rdparty/bootstrap-5.1.3-dist/js/bootstrap.bundle.js',
            'js/autocomplete.js'
        ]

    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}
        self.placeholder = kwargs.get("placeholder", self.placeholder)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["placeholder"] = value or self.placeholder
        # TODO: Don't like using name.split("__prefix__-", 1)[1] to get the field name from within widget template.
        if "__prefix__" in name:
            context["widget"]["field_name"] = name.split("__prefix__-", 1)[1]
        else:
            context["widget"]["field_name"] = name
        return context
