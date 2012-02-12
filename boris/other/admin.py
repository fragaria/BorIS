from django.contrib import admin
from boris.other.models import SyringeCollection
from boris.utils.admin import BorisBaseAdmin


class SyringeCollectionAdmin(BorisBaseAdmin):

    raw_id_fields = ('town', 'persons',)
    autocomplete_lookup_fields = {
        'fk': ['town', ],
        'm2m': ['persons', ],
    }

    class Meta:
        model = SyringeCollection


admin.site.register(SyringeCollection, SyringeCollectionAdmin)
