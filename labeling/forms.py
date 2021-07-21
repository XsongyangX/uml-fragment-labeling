from labeling.sampler import Sampler
from django import forms

from .models import Label

class LabelForm(forms.Form):
    description = forms.CharField(label='Description', max_length=500, widget=forms.Textarea)

    def process(self, fragment):

        # check if already labeled
        try:
            Label.objects.get(fragment=fragment)
        except Label.DoesNotExist:
            pass
        else:
            raise DuplicateLabelException

        Label.objects.create(label=self.cleaned_data["description"], fragment=fragment)
        Sampler.current_class_count = fragment.model.classes

class DuplicateLabelException(Exception):
    pass