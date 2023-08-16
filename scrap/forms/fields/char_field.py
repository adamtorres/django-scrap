from django import forms


class CharField(forms.CharField):
    """
    Character field with my most common defaults.
    """
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = kwargs.get("max_length", 1024)
        kwargs["required"] = kwargs.get("required", False)
        kwargs["empty_value"] = kwargs.get("empty_value", "")
        super().__init__(*args, **kwargs)
