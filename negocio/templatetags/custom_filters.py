from django import template

register = template.Library()

@register.filter
def to(value):
    """Genera una lista de números desde 1 hasta el valor de 'value'."""
    return range(1, value + 1)
