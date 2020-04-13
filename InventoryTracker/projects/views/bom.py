from django.views.generic.base import TemplateView
from django.http import Http404

from projects.forms import BOMUploadSelectForm
from projects.models import ProjectPartModel

class ProjectBOMView(TemplateView):
    """
    Project index  templated view
    """
    template_name = "projects/bom.html"

    def get(self, request, *args, **kwargs):
        if not 'id' in kwargs:
            raise Http404

        self._ID: int =int(kwargs['id'])

        self._ProjectParts = ProjectPartModel.objects.filter(Project__pk = self._ID)
        self._ProjectParts = self._ProjectParts.order_by('Part__Name')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload_form'] = BOMUploadSelectForm()
        context['title'] = "BOM"
        context['Parts'] = self._ProjectParts
        context['ID'] = self._ID
        return context
