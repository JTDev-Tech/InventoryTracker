from typing import Optional
from django.views.generic.base import TemplateView
from django.forms import Form
from django.shortcuts import redirect
from projects.models import ProjectModel
from projects.forms import AddProjectForm

class ProjectAddView(TemplateView):
    """
    Project index  templated view
    """
    template_name = "projects/add.html"

    def __init__(self, **kwargs):
        self.__Form: Optional[Form] = None;

        return super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.__Form = AddProjectForm()
        return super().get(request, *args, **kwargs)

    def post(self, request, **kwargs):
        self.__Form = AddProjectForm(request.POST)
        if self.__Form.is_valid():
            try:
                m = ProjectModel(Name=self.__Form.cleaned_data['Name'],
                                 Description = self.__Form.cleaned_data['Description'])
                m.save()

                return redirect("projects:home")
            except:
                raise

        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.__Form
        context['title'] = "Projects"
        return context
