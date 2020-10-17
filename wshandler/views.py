from django.shortcuts import render


def index(request):
    """
    this function serve only index file
    """
    return render(request, "index.html", {})
