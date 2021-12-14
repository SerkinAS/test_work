"""Urls проекта."""
from django.contrib import admin
from django.urls import include
from django.urls import path

from .views import shortened_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shortened_url.urls')),
    path('<str:short_url>/', shortened_redirect, name='shortened_redirect'),
    path('<str:subpath>/<str:short_url>/',
         shortened_redirect, name='subpath_redirect'),
]
