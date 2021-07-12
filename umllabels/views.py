from django.shortcuts import render

from labeling.models import Fragment, Label, Model

# Home index

def index(request):
    context = {
        "total_models": Model.objects.all().filter(classes__gt=0).count(),
        "total_fragments": Fragment.objects.count(),
        "models_done": Model.objects.filter(
            fragment__label__isnull=False
        ).count(),
        "fragments_done": Label.objects.count()
    }
    return render(request, "umllabels/index.html", context=context)