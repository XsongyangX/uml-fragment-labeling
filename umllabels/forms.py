from django import forms

from labeling.models import Label

class ValidationForm(forms.Form):
    isAcceptable = forms.BooleanField(required=False, label="This label is acceptable.", initial=True)