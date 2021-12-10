"""Представления приложения shortened_url."""
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response

from test_django_work.settings import CACHE_TTL

from .models import UrlShort
from .serializers import UrlSerializer


class UrlShortView(generics.ListCreateAPIView):
    """Представление модели UrlShort."""

    serializer_class = UrlSerializer

    def get(self, request):
        """Get-запрос для экземпляров модели UrlShort."""
        # Если в кэше нет id сессии, добавим её.
        if request.session.session_key != cache.get('session'):
            # Поместим session_id в кэш.
            cache.set('session', request.session.session_key)
        # Возвращаем объекты только для текущей сессии.
        urls = UrlShort.objects.filter(session_id=cache.get('session'))
        serializer = UrlSerializer(urls, many=True)
        return Response({'Urls': serializer.data})

    def post(self, request, *args, **kwargs):
        """Отправка post-запроса."""
        # Если в кэше нет id сессии, добавим её.
        if request.session.session_key != cache.get('session'):
            # Поместим session_id в кэш.
            cache.set('session', request.session.session_key)
        serializer = UrlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        # Занесём в кэш основные атрибуты модели с таймаутом.
        cache.set(
            serializer.data['full_url'],
            dict(
                full_url=serializer.data['full_url'],
                short_url=serializer.data['short_url']
            ),
            timeout=CACHE_TTL
        )
        urls = UrlShort.objects.filter(session_id=cache.get('session'))
        serializer = UrlSerializer(urls, many=True)
        return Response({'Urls': serializer.data})


class UrlShortDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
        generics.GenericAPIView):
    """Представление для просмотра отдельных записей и их удаления."""

    queryset = UrlShort.objects.all()
    serializer_class = UrlSerializer

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(UrlShort, id=kwargs['pk'])
        # Удалим и из кэша.
        cache.delete(obj.full_url)
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
