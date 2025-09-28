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

@register.filter
def add_class(bound_field, css_class):
    """Add CSS class to form field"""
    if 'class' in bound_field.field.widget.attrs:
        bound_field.field.widget.attrs['class'] += ' ' + css_class
    else:
        bound_field.field.widget.attrs['class'] = css_class
    return bound_field

@register.filter
def attr(bound_field, attr_string):
    """Add arbitrary attribute to form field, e.g., 'aria-describedby: id_help'"""
    if ':' in attr_string:
        key, value = attr_string.split(':', 1)
        key = key.strip()
        value = value.strip()
        bound_field.field.widget.attrs[key] = value
    return bound_field
