from django import forms
from .models import ProjectModel

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['Name', 'Description']

class BOMUploadSelectForm(forms.Form):
    BOMFile = forms.FileField(help_text="BOM file to upload")

