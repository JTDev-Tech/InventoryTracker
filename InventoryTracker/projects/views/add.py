from django.views.generic.base import TemplateView

class ProjectAddView(TemplateView):
    """
    Project index  templated view
    """
    template_name = "projects/add.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Projects"
        return context
