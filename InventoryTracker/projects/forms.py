from django import forms
from .models import ProjectModel

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['Name', 'Description']
