from django import forms


class AutocompleteWidget(forms.widgets.TextInput):
    template_name = "scrap/forms/widgets/autocomplete.html"
    placeholder = "needs a value"

    class Media:
        css = {
            'all': ('3rdparty/bootstrap-5.1.3-dist/css/bootstrap.min.css', )
        }
        js = [
            '3rdparty/js/jquery-3.6.0.min.js', '3rdparty/bootstrap-5.1.3-dist/js/bootstrap.bundle.min.js',
            'js/autocomplete.js'
        ]

    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}
        self.placeholder = kwargs.get("placeholder", self.placeholder)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["placeholder"] = value or self.placeholder
        return context
