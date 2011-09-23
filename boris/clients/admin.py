from django.contrib import admin

from boris.clients.models import Client, Drug, ClientNote, Town

admin.site.register(Client)
admin.site.register(ClientNote)
admin.site.register(Drug)
admin.site.register(Town)

