from django.shortcuts import render
# Home index

def index(request):
    return render(request, "umllabels/index.html")