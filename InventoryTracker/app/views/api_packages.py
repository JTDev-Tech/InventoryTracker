from django.http import HttpRequest, JsonResponse 

from app.models import PackageModel

def api_packages(request):
	assert isinstance(request, HttpRequest)
	Result = list()

	for p in PackageModel.objects.all():
		t = {
			"ID":p.id,
			"Name":p.Name,
			"Ref":p.Reference,
			}

		Result.append(t)

	return JsonResponse(Result, safe=False)
