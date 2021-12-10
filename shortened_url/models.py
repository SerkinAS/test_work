"""Модели приложения shortened_url."""
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


class UrlShort(models.Model):
    """Модель UrlShort."""

    full_url = models.URLField(verbose_name='Полный URL', unique=True)
    short_url = models.CharField(
        verbose_name='Сокращённый URL',
        unique=True,
        max_length=80,
    )
    session_id = models.CharField(
        verbose_name='id сессии',
        max_length=80,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания записи',
        auto_now_add=True
    )

    def __str__(self):
        """Представление объектов кверисета."""
        return f'{self.short_url}({self.id})'

    def save(self, *args, **kwargs):
        """Сохранение объекта."""
        validate = URLValidator()
        # Проверка валидации full_url.
        try:
            validate(self.full_url)
        except ValidationError as e:
            raise ValidationError('Invalid full-url')
        # Проверим наличие сокращённого url.
        try:
            UrlShort.objects.filter(
                short_url=self.short_url
            ).exists()
        except ValidationError as e:
            raise ValidationError(
                f'Short-url {self.short_url} уже существует.'
            )
        self.session_id = cache.get('session')
        return super().save(*args, **kwargs)
