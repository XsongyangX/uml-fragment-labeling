from django import forms

from .models import Label

class LabelForm(forms.Form):
    description = forms.CharField(label='Description', max_length=500, widget=forms.Textarea)

    def process(self, fragment):
        Label.objects.create(label=self.cleaned_data["description"], fragment=fragment)