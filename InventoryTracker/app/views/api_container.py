from django.http import HttpRequest, JsonResponse 

from app.models import ContainerModel

def api_container(request):
	assert isinstance(request, HttpRequest)
	Result = list()

	for c in ContainerModel.objects.all():
		t = {
			"ID":c.id,
			"Name":c.Name,
			}

		Result.append(t)

	return JsonResponse(Result, safe=False)
