from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.simple_tag
def substringFilter(arg1):
    re.sub(r'<\/?.+?>', '', arg1)
    return re.sub(r' ','', re.sub(r'<\/?.+?>', '', arg1))[0:300]+'...'

@register.simple_tag
def list2String(arg1):
    return ','.join(arg1)
