"""Сериализаторы приложения."""
from rest_framework import serializers

from shortened_url.models import UrlShort


class UrlSerializer(serializers.Serializer):
    """Сериализация для модели UrlShort."""

    full_url = serializers.URLField()
    short_url = serializers.CharField()

    def create(self, validated_data):
        """Создание объекта модели.
        :param: validated_data - данные с формы.
        """
        return UrlShort.objects.create(**validated_data)
