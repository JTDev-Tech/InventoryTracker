from django.shortcuts import render
from django.http import HttpRequest
from app.models import PartModel

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    all = PartModel.objects.all().order_by('Category')
    return render(
        request,
        'app/index.html',
        {
            'parts': all,
            'title':'Home Page',
        }
    )

