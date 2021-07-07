from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Label, Fragment, Model

class IndexView(generic.ListView):
    model = Label
    template_name = 'labeling/index.html'