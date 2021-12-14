"""Представления основного приложения."""
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from shortened_url.models import UrlShort


def shortened_redirect(request, subpath=None, short_url=None):
    """Представление для редиректа по сокращённому url."""
    cache_rule = cache.get(f'{request.session.session_key}_{short_url}')
    # Если правило есть в кэше, возьмём его full_url для редиректа.
    if cache_rule:
        full_url = cache_rule['full_url']
    # Иначе обратимся к базе данных.
    else:
        full_url = get_object_or_404(UrlShort, short_url=short_url).full_url
    return redirect(full_url)
