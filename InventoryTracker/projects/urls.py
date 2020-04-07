from django.urls import path
from django.conf.urls import include, url

from . import views

app_name = 'projects'
urlpatterns = [
    path('bom/<int:id>', views.ProjectBOMView.as_view(), name='bom'),
    path('add', views.ProjectAddView.as_view(), name='add'),
    path('', views.ProjectIndexView.as_view(), name='home'),
]

