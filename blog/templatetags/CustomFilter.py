from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def substringFilter(arg1):
    return arg1[0:300]+'...'

@register.simple_tag
def list2String(arg1):
    return ','.join(arg1)
