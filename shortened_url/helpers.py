"""Вспомогательные функции."""
import re

from django.core.cache import cache


def short_str_parser(short_url_string):
    """Парсер для извлечения из строки subpath и short_url."""
    subpath = ''
    parsed_list = re.split('/', short_url_string)
    if parsed_list.__len__() == 1:
        short_url = parsed_list[0]
    else:
        subpath = get_subpath(short_url_string)
        short_url = get_short_str(short_url_string)
    return subpath, short_url


def get_subpath(string):
    """Извлекает subpath из строки."""
    if string.split('/').__len__() == 1:
        result = string
    else:
        result = string.split('/')[:string.split('/').__len__() - 1][0]
    return result


def get_short_str(string):
    """Извлекает short_url без доп. пути."""
    return string.split('/')[string.split('/').__len__() - 1:][0]


def get_cache_rules(prefix_key):
    """Поиск сохранённых правил в кэше."""
    cache_rules_list = []
    for key in cache.keys(prefix_key):
        cache_rules_list.append(cache.get(key))
    return cache_rules_list
