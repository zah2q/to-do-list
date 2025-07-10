# tasks/templatetags/math_filters.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """يضرب القيمة في المعامل"""
    return value * arg

@register.filter
def div(value, arg):
    """يقسم القيمة على المعامل"""
    if arg == 0:
        return 0
    return value / arg