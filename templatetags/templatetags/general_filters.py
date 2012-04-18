import datetime, pytz, re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter("hash_num")
def hash_num(value, arg):
    s = force_unicode(value)
    try:
        value.isdigit()
    except: 
        return value
hash_num.is_safe = True
