from umllabels.forms import ValidationForm
from django.shortcuts import redirect, render
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden

from labeling.models import Fragment, Label, Model

# Home index

def index(request):
    context = {
        "total_models": Model.objects.all().filter(classes__gt=0).count(),
        "total_fragments": Fragment.objects.count(),
        "models_done": Model.objects.filter(
            fragment__label__isnull=False
        ).distinct().count(),
        "fragments_done": Label.objects.count()
    }
    return render(request, "umllabels/index.html", context=context)

def validation(request):

    # get a label
    label : Label = Label.objects.filter(validated=False).first()

    if label == None:
        # No more labels to validate
        return HttpResponse(f"All received labels are validated. Back to <a href='/'>Menu</a>.")

    fragment : Fragment = label.fragment
    model : Model = fragment.model

    context = {
        "label": label.label,
        "shown_model_name":  model.name,
        "fragment_kind": fragment.kind,
        "fragment_number": fragment.number,
        "form": ValidationForm(),
        "shown_fragment": f"fragments/{fragment}.png",
        "shown_model": f"fragments/{model}.png",
    }
    return render(request, "umllabels/validation.html", context=context)

def get_form(request, model, kind, number):

    # form
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ValidationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            fragment = Fragment.objects.get(
                model=Model.objects.get(name=model),
                number=number,
                kind=kind
            )
            label : Label = Label.objects.get(fragment=fragment)

            # process the data in form.cleaned_data as required
            if form.cleaned_data["isAcceptable"]:
                label.validated = True
                label.save()

            else:
                # delete the label
                label.delete()

            return redirect('/validation/')

    # if a GET (or any other method) we throw an error
    else:
        return HttpResponseForbidden(content="You cannot come here")