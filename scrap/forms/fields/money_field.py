from django import forms


class MoneyField(forms.DecimalField):
    """
    Decimal field with my most common defaults.  Separate from DecimalField in case there's something money-specific.
    """
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = kwargs.get("max_digits", 10)
        kwargs["decimal_places"] = kwargs.get("decimal_places", 4)
        kwargs["required"] = kwargs.get("required", False)
        # kwargs["default"] = kwargs.get("default", 0)
        super().__init__(*args, **kwargs)
