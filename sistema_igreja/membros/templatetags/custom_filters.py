# membros/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Retorna o valor de uma chave específica de um dicionário.
    Uso: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)