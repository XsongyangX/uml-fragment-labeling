from labeling.sampler import Sampler
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Label, Fragment, Model

from .forms import LabelForm

def index(request):

    form = LabelForm()

    model, fragment = Sampler.next()

    # check for end conditions
    if model == None and fragment == None:
        return HttpResponse("Labeling complete!")
    elif model == None and fragment != None:
        return HttpResponseForbidden("No model but there is a fragment!")
    elif model != None and fragment == None:
        return HttpResponseForbidden("No fragment on this model")
    else:
        pass # business as usual

    context = {
        "shown_model": f"fragments/{model.name}.png",
        "shown_model_name": model.name,
        "shown_fragment": f"fragments/{model.name}_{fragment.kind}{fragment.number}.png",
        "fragment_kind": fragment.kind,
        "fragment_number": fragment.number,
        "form": form
    }
    return render(request, "labeling/index.html", context=context)

def get_form(request, model, kind, number):
    
    # form
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LabelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            fragment = Fragment.objects.get(
                model=Model.objects.get(name=model),
                number=number,
                kind=kind
            )
            form.process(fragment)

            return HttpResponseRedirect('/labeling/')

    # if a GET (or any other method) we throw an error
    else:
        return HttpResponseForbidden(content="You cannot come here")