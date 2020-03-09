from django.urls import path
from django.conf.urls import include, url
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('add_part', views.add_part, name='add_part'),
    path('add_part/c', views.add_part_capacitor, name='add_part_capacitor'),
    path('add_part/r', views.add_part_resistor, name='add_part_resistor'),
]
