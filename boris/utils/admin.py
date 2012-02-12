'''
Created on 12.2.2012

@author: xaralis
'''
from django.contrib.admin.options import ModelAdmin
from django.utils.translation import ugettext_lazy as _

class BorisBaseAdmin(ModelAdmin):
    def __init__(self, *args, **kwargs):
        self.list_display += ('change_link',)
        super(BorisBaseAdmin, self).__init__(*args, **kwargs)
        self.list_display_links += ('change_link',)

    def change_link(self, obj):
        return u'<a href="%s" class="changelink cbutton">%s</button>' % (
            obj.get_admin_url(), _('upravit'))
    change_link.allow_tags = True
    change_link.short_description = _('Upravit')
