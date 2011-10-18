# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse
from django.utils.formats import get_format
from django.utils.translation import ugettext as _
from anyjson import serialize

from boris.clients.models import ClientNote
from boris.clients.forms import ClientNoteForm


def add_note(request):
    if not request.method == 'POST' or not request.is_ajax():
        raise Http404

    form = ClientNoteForm(request.POST)

    if not form.is_valid():
        if 'datetime' in form.errors:
            err_msg = _(u'Zadejte prosím platné datum a čas.')
        elif 'text' in form.errors:
            err_msg = _(u'Zadejte prosím neprázdný text.')
        elif 'client' in form.errors:
            err_msg = _(u'Zadaný klient neexistuje. (Nebyl mezitím smazán?)')

        return HttpResponse(serialize({'error': err_msg}))

    client_note = form.save(commit=False)
    client_note.author = request.user
    client_note.save()

    ret = {
        'id': client_note.pk,
        'author': client_note.author.username,
        'datetime': format(client_note.datetime, get_format('DATE_FORMAT')),
        'text': client_note.text,
    }

    return HttpResponse(serialize(ret))

def delete_note(request, note_id):
    if not request.is_ajax():
        raise Http404

    ClientNote.objects.filter(pk=note_id).delete()

    return HttpResponse('OK')

