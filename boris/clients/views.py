from anyjson import serialize

from django.http import HttpResponse, HttpResponseBadRequest

from boris.clients.models import ClientNote, Client

def add_client_note(request):
    if request.POST and request.POST.get('text') and \
            request.user.is_authenticated() and request.is_ajax():

        try:
            client = Client.objects.get(pk=int(request.POST.get('client', -1)))
        except (Client.DoesNotExist, ValueError):
            return HttpResponseBadRequest()

        client_note = ClientNote(author=request.user, text=request.POST['text'], client=client)
        client_note.save()

        ret = {
            'author': client_note.author.username,
            'datetime': client_note.datetime.strftime('%d.%m.%Y %H:%M'),
            'text': client_note.text,
        }

        return HttpResponse(serialize(ret))
    else:
        return HttpResponseBadRequest()

