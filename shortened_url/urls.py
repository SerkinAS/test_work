"""Url's приложения shortened_url."""
from django.urls import path
from shortened_url.views import UrlShortView, UrlShortDetail


urlpatterns = [
    path('urls/', UrlShortView.as_view()),
    path('urls/<int:pk>', UrlShortDetail.as_view())
]
