from django import template

from ..models import Menu  # los puntos son para moverte en los directorios

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    return Menu.objects.get(slug=slug)
