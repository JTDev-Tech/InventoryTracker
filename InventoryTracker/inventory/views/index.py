from django.shortcuts import render
from django.http import HttpRequest

from inventory.models import PartModel

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    all = PartModel.objects.all().order_by('Category')
    return render(
        request,
        'inventory/index.html',
        {
            'parts': all,
            'title':'Home Page',
        }
    )

