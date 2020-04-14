"""
Definition of urls for InventoryTracker.
"""
from typing import Union, List

from django.urls import path, URLPattern, URLResolver
from django.conf.urls import include, url
from django.contrib import admin
from app.views import index
from django.conf import settings
from django.conf.urls.static import static


urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('', index, name='index'),
    path('inv/', include('inventory.urls')),
    path('proj/', include('projects.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

