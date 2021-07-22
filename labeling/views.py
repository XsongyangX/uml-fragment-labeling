from labeling.sampler import Sampler
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Label, Fragment, Model

from .forms import DuplicateLabelException, LabelForm

def index(request, model=None, fragment=None):

    form = LabelForm()

    if model == None or fragment == None:
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

    # more models
    more_models = Sampler.more_models(5, exclude=model)
    more_fragments = Sampler.more_fragments(model=model, limit=5)

    more = []

    for m in more_models:
        incomplete_fragment = Fragment.objects.filter(model=m, label__isnull=True).first()
        more.append({
            "filter": "nature", # nature for models
            "image": f"fragments/{m.name}.png",
            "caption_header": m.name,
            "caption": f"{m.classes} classes, {m.relations} relations",
            "model": m.name,
            "kind": incomplete_fragment.kind,
            "number": incomplete_fragment.number,
        })

    for f in more_fragments:
        more.append({
            "filter": "animals", # nature for models
            "image": f"fragments/{f}.png",
            "caption_header": f"Fragment",
            "caption": f"{f.kind} {f.number}",
            "model": model.name,
            "kind": f.kind,
            "number": f.number,
        })

    context = {
        "shown_model": f"fragments/{model.name}.png",
        "shown_model_name": model.name,
        "shown_fragment": f"fragments/{model.name}_{fragment.kind}{fragment.number}.png",
        "fragment_kind": fragment.kind,
        "fragment_number": fragment.number,
        "form": form,
        "more": more
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
            try:
                form.process(fragment)
            except DuplicateLabelException:
                return HttpResponse(f"An existing label already exists for {fragment}. Back to <a href='/'>Menu</a>.")

            return HttpResponseRedirect('/labeling/')

    # if a GET (or any other method) we throw an error
    else:
        return HttpResponseForbidden(content="You cannot come here")

def specific(request, model, kind, number):
    model = Model.objects.get(name=model)
    fragment = Fragment.objects.get(model=model, kind=kind, number=number)
    return index(request, model=model, fragment=fragment)