"""Представления основного приложения."""
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from shortened_url.models import UrlShort


def shortened_redirect(request, short_url):
    """Представление для редиректа по сокращённому url."""
    url = get_object_or_404(UrlShort, short_url=short_url)
    return redirect(url.full_url)
