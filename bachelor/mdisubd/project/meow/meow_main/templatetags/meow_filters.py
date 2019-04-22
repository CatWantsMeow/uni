from django import template


register = template.Library()


@register.filter
def encode(string):
    return string.encode('utf-8')