"""Представления приложения shortened_url."""
import datetime

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response

from test_django_work.settings import CACHE_TTL

from .helpers import get_cache_rules
from .helpers import get_subpath
from .models import UrlShort
from .serializers import UrlSerializer


class UrlShortView(generics.ListCreateAPIView):
    """Представление модели UrlShort."""

    serializer_class = UrlSerializer

    def get(self, request):
        """Get-запрос для экземпляров модели UrlShort."""
        # Если в кэше нет id сессии, добавим её.
        if request.session.session_key != cache.get('session'):
            # Поместим id сессии в кэш.
            cache.set('session', request.session.session_key)
        # Префикс ключа для поиска правил в кэше.
        prefix_key = cache.get('session') + '*'
        cache_rules = get_cache_rules(prefix_key)
        # Если в кэше нет объектов, обратимся к базе данных.
        if cache_rules:
            data = cache_rules
        else:
            # Возвращаем объекты только для текущей сессии в случае,
            # если в кэше пусто.
            urls = UrlShort.objects.filter(session_id=cache.get('session'))
            serializer = UrlSerializer(urls, many=True)
            data = serializer.data
        return Response({'ShortUrls': data})

    def post(self, request, *args, **kwargs):
        """Отправка post-запроса."""
        # Если в кэше нет id сессии, добавим её.
        cache_session = cache.get('session')
        if request.session.session_key != cache_session:
            # Поместим id сессии в кэш.
            cache.set('session', request.session.session_key)
        serializer = UrlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Так как модель на этом этапе была сохранена, теперь
            # занесём в кэш основные атрибуты модели с таймаутом.
            cache.set(
                # Сессию сделаем префиксом ключа для дальнейшей работы.
                f'{cache_session}_%s' % serializer.data['short_url'],
                dict(
                    full_url=serializer.data['full_url'],
                    short_url=serializer.data['short_url'],
                    subpath=get_subpath(request.data['short_url']),
                    created_at=datetime.datetime.now(),
                ),
                timeout=CACHE_TTL
            )
        cache_rules = get_cache_rules(cache.get('session') + '*')
        if cache_rules:
            data = cache_rules
        else:
            urls = UrlShort.objects.filter(session_id=cache.get('session'))
            serializer = UrlSerializer(urls, many=True)
            data = serializer.data
        return Response({'ShortUrls': data})


class UrlShortDetail(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    """Представление для просмотра отдельных записей и их удаления."""

    queryset = UrlShort.objects.all()
    serializer_class = UrlSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(UrlShort, id=kwargs['pk'])
        key = '%s_%s' % (cache.get('session'), obj.short_url)
        # Удалим правило из кэша.
        cache.delete(key)
        return self.destroy(request, *args, **kwargs)
