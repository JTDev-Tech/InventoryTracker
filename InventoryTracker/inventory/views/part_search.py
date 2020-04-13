from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from inventory.models import PartModel

class PartSearch(View):
    """
    Returns a JSON list of parts that match the provided search term
    """

    def get(self, request)->JsonResponse:
        Term =  request.GET.get('term', '')
        ModelSet = PartModel.objects.filter(Q(Name__istartswith = Term) | Q(Category__CategoryName__istartswith=Term))
        Res = list()
        for m in ModelSet.order_by('pk'):
            Item = dict()
            Item['cat_name'] = m.Category.CategoryName
            Item['label'] = m.GetValue()
            Item['value'] = m.pk
            Res.append(Item)

        return JsonResponse(Res, safe=False)
