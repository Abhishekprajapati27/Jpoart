from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split a string by the given argument"""
    if not value:
        return []
    return str(value).split(arg)

@register.filter
def trim(value):
    """Remove leading and trailing whitespace"""
    if not value:
        return value
    return str(value).strip()
