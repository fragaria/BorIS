'''
Created on 2.10.2011

@author: xaralis
'''
from django.shortcuts import render, get_object_or_404
from boris.clients.models import Client
from boris.services.models.core import get_model_for_class_name, ClientService
from django.core.urlresolvers import reverse
import anyjson
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.template.context import RequestContext

class HandleForm(object):
    def get_context(self, request, client_id, service_cls, object_id):
        cls = get_model_for_class_name(service_cls)
        client = get_object_or_404(Client, pk=client_id)
        ctx = {
            'client': client,
            'cls': service_cls,
            'service': cls,
            'is_edit': object_id is not None
        }
        kwargs = {}
        
        if ctx['is_edit']:
            obj = get_object_or_404(cls, pk=object_id)
            ctx.update({
                'obj': obj,
                'action_link': reverse('services_handle_form_change', kwargs={
                    'client_id': client_id, 'service_cls': service_cls, 'object_id': object_id
                })
            })
            kwargs['instance'] = obj
        else:
            ctx.update({
                'action_link': reverse('services_handle_form_add', kwargs={
                    'client_id': client_id, 'service_cls': service_cls
                })
            })
            
        if request.method == 'POST':
            form = cls.form()(client, request.POST, **kwargs)
        else:
            form = cls.form()(client, **kwargs)
        ctx.update({'form': form})
        return ctx

    def __call__(self, request, client_id, service_cls, object_id=None):
        ctx = self.get_context(request, client_id, service_cls, object_id)
        
        if request.method == 'POST':
            form = ctx['form']
            resp = {}
            if form.is_valid():
                form.save()
                resp['ok'] = True
            else:
                resp.update({
                    'ok': False,
                    'content': render_to_string(form.template_list, ctx,
                        context_instance=RequestContext(request))
                })
            return HttpResponse(anyjson.dumps(resp), mimetype='application/json')
        else:
            return render(request, ctx['form'].template_list, ctx)
        
handle_form = HandleForm()

def services_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    services_done = ClientService.objects.filter(client=client)
    return render(request, 'services/list.html', {'client': client,
        'services_done': services_done})
    
def drop_service(request, service_id):
    try:
        service = ClientService.objects.select_subclasses().filter(pk=service_id)[0]
        service.delete()
        return HttpResponse('OK')
    except IndexError:
        raise Http404
    