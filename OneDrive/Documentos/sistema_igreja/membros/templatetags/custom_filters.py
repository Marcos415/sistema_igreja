from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Retorna o valor de um dicionário para uma chave específica.
    Permite usar a sintaxe `dicionario|get_item:chave` em templates.
    """
    return dictionary.get(key)
