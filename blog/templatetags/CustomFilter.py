from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re, datetime, pytz, time

register = template.Library()

@register.simple_tag
def substringFilter(arg1, arg2):
    re.sub(r'<\/?.+?>', '', arg1)
    ret = arg1
    if len(arg1) > arg2:
        ret = re.sub(r' ','', re.sub(r'<\/?.+?>', '', arg1))[0:arg2]+'...'
    return ret

@register.simple_tag
def list2String(arg1):
    return ','.join(arg1)

@register.simple_tag
def utc_to_local(utc_time_str):
    print(utc_time_str)
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_time_str + offset
    return local_st.strftime("%Y-%m-%d")

