from django.urls import path
from django.conf.urls import include, url
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('add_part', views.AddPartBaseView.as_view(), name='add_part'),
    path('add_part/c', views.AddCapacitorView.as_view(), name='add_part_capacitor'),
    path('add_part/r', views.AddResistorView.as_view(), name='add_part_resistor'),

    path('projects', views.ProjectIndexView.as_view(), name='projects'),
    path('projects/<int:id>/bom', views.ProjectBOMView.as_view(), name='bom'),
]
