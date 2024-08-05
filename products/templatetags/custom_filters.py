from django import template
import re

register = template.Library()

@register.filter
def split_last(value):
    """
    Разделяет строку на две части: все, кроме последнего слова/фразы, и последнее слово/фразу.
    """
    # Разделяем строку на все кроме последнего слова/фразы
    match = re.search(r'(.*)\s+(\S+)$', value)
    if match:
        return match.groups()
    else:
        return (value, '')
