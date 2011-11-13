'''
Created on 2.10.2011

@author: xaralis
'''
from django import template
from boris.services.models.core import service_list

register = template.Library()

@register.inclusion_tag('services/interface.html')
def render_service_interface(encounter):
    return {
        'encounter': encounter,
        'services_done': encounter.services.all(),
        'service_list': service_list(encounter.client)
    }