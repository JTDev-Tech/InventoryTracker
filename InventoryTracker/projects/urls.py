from django.urls import path
from django.conf.urls import include, url

from . import views

app_name = 'projects'
urlpatterns = [
    path('<int:id>/bom', views.ProjectBOMView.as_view(), name='bom'),
    path('add', views.ProjectAddView.as_view(), name='add'),
    path('<int:id>/bom_upload', views.BomUpload.as_view(), name="csv_upload"),
    path('', views.ProjectIndexView.as_view(), name='home'),
]

