from labeling.sampler import Sampler
from django import forms

from .models import Label

class LabelForm(forms.Form):
    not_in_english = forms.BooleanField(required=False, label="This fragment/model is not in English.", help_text="\n", initial=False)
    description = forms.CharField(label='Description', max_length=500, widget=forms.Textarea)
    def process(self, fragment):

        # check if already labeled
        try:
            Label.objects.get(fragment=fragment)
        except Label.DoesNotExist:
            pass
        else:
            raise DuplicateLabelException

        Label.objects.create(label=self.cleaned_data["description"], fragment=fragment, in_english=not self.cleaned_data["not_in_english"])
        Sampler.current_class_count = fragment.model.classes

class DuplicateLabelException(Exception):
    pass