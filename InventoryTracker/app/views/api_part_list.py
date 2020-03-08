from django.shortcuts import render
from django.http import HttpRequest, JsonResponse 
from datetime import datetime

from app.models import PartModel

def api_part_list(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    Result = list()
    for f in PartModel.objects.all():

        ContList = list()
        for c in f.partcountmodel_set.all():
            ShelfDict = c.Location.Shelf.ToJsonDict()
                
            ContList.append({
                "ID":c.id,
                "Count":c.Quantity,
                "Location":c.Location.Name,
                "Shelf":ShelfDict,
                })

        t = {'Name':f.Name,
             'Category':{'Id':f.Catagory.id, 'Name':f.Catagory.CatagoryName},
             'Package':{'ID':f.Package.id, 'Name':f.Package.Name},
             'Containers':ContList
             }
        Result.append(t)

    return JsonResponse(Result, safe=False)
