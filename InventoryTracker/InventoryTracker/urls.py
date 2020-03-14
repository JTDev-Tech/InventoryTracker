"""
Definition of urls for InventoryTracker.
"""

from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from app.views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^inv/', include('inventory.urls')),
    url(r'^proj/', include('projects.urls')),
    path('admin/', admin.site.urls),
]
