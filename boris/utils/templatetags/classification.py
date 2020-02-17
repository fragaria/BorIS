from django import template
from django.utils.safestring import mark_safe

from boris import classification

register = template.Library()


@register.simple_tag
def get_non_application_drugs():
    return mark_safe(str(classification.NON_APPLICATION_DRUGS))
