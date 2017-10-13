# -*- coding: utf-8 -*-
from datetime import datetime
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.formats import get_format
from django.utils.dateformat import format
from django.utils.translation import ugettext as _
from anyjson import serialize

from boris.clients.models import ClientNote
from boris.clients.forms import ClientNoteForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404


def add_note(request):
    """
    An ajax view for adding notes to the clients in admin.
    """
    if not request.method == 'POST' or not request.is_ajax():
        raise Http404

    form = ClientNoteForm(request.POST)

    if not form.is_valid():
        if 'datetime' in form.errors:
            err_msg = _(u'Zadejte prosím platný datum a čas.')
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
        'datetime_iso': client_note.datetime.isoformat(),
        'datetime_formatted': format(client_note.datetime, get_format('DATETIME_FORMAT')),
        'text': client_note.text,
    }

    return HttpResponse(serialize(ret))


def edit_note(request, note_id):
    note = ClientNote.objects.get(id=note_id)
    note.text = request.POST['text']
    note.datetime = datetime.strptime(request.POST['datetime'], '%d.%m.%Y %H:%M')
    note.save()
    return JsonResponse({
        'text': note.text,
        'author': note.author_id,
        'datetime_iso': note.datetime.isoformat(),
        'datetime_formatted': format(note.datetime, get_format('DATETIME_FORMAT'))
    })


@permission_required('clients.delete_clientnote')
def delete_note(request, note_id):
    """
    An ajax view for deleting client notes in admin.
    """
    if not request.is_ajax():
        raise Http404

    note = get_object_or_404(ClientNote, pk=note_id)

    if request.user.is_superuser or note.author == request.user:
        note.delete()
        return HttpResponse('OK')

