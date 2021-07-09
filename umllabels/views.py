from django.shortcuts import render
# Home index

def index(request):
    context = {
        "total_models": 289,
        "total_fragments": 8215,
        "models_done": 0,
        "fragments_done": 0
    }
    return render(request, "umllabels/index.html", context=context)