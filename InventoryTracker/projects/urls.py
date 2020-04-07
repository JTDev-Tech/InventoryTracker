from django.urls import path
from django.conf.urls import include, url

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.ProjectIndexView.as_view(), name='home'),
    path('add', views.ProjectIndexView.as_view(), name='add'),
]

