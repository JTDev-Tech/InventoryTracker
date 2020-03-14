"""
Definition of urls for InventoryTracker.
"""

from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from app.views import index

urlpatterns = [
    path('', index, name='index'),
    path('inv/', include('inventory.urls')),
    path('proj/', include('projects.urls')),
    path('admin/', admin.site.urls),
]
