"""
Definition of urls for InventoryTracker.
"""
from typing import Union, List

from django.urls import path, URLPattern, URLResolver
from django.conf.urls import include, url
from django.contrib import admin
from app.views import index

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('', index, name='index'),
    path('inv/', include('inventory.urls')),
    path('proj/', include('projects.urls')),
    path('admin/', admin.site.urls),
]

