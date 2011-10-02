'''
Created on 2.10.2011

@author: xaralis
'''
from django import template
from boris.services.models.core import service_list

register = template.Library()

@register.inclusion_tag('services/interface.html')
def render_service_interface(client):
    return {
        'client': client,
        'services_done': client.services.all(),
        'service_list': service_list(client)
    }