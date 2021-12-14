"""Модели приложения shortened_url."""
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.db.models import Q

from shortened_url.helpers import short_str_parser


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
    subpath = models.CharField(
        verbose_name='Дополнительный путь',
        max_length=60,
        default='',
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
        except ValidationError:
            raise ValidationError('Invalid full-url')
        # Определим доп. путь и сокращённый url.
        self.subpath, self.short_url = short_str_parser(self.short_url)
        # Проверим наличие сокращённого url в базе данных.
        if UrlShort.objects.filter(short_url=self.short_url).exists():
            raise ValidationError(
                f'Short_url {self.short_url} уже существует.'
            )
        if UrlShort.objects.filter(
            Q(subpath=self.subpath) & ~Q(subpath='')
        ).exists():
            raise ValidationError(
                f'Subpath {self.subpath} уже существует.'
            )
        self.session_id = cache.get('session')
        return super().save(*args, **kwargs)
