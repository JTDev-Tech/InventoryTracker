from django.views.generic.base import TemplateView

from projects.models import ProjectModel

class ProjectIndexView(TemplateView):
    """
    Project index  templated view
    """
    template_name = "projects/project_index.html"

    def get(self, request, *args, **kwargs):
        self._Projects = ProjectModel.objects.all().order_by('Name')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Projects"
        context['Projects'] = self._Projects
        return context