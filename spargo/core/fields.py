from django import forms

from .utils import normalize_phone
from .validators import validate_mobile_phone


class MobileNumberField(forms.Field):
    def clean(self, value):
        super(MobileNumberField, self).clean(value)
        if value:
            validate_mobile_phone(value)
            return normalize_phone(value)
        else:
            return value
