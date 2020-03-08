"""
Definition of urls for InventoryTracker.
"""

from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('app.urls')),
    path('admin/', admin.site.urls),
    #url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
]
