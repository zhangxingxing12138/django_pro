from django.template import Library
register=Library()

@register.filter
def mod(values ,value2):
    return values % value2 == 0

