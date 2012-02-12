'''
Created on 12.2.2012

@author: xaralis
'''
from django.contrib.admin.options import ModelAdmin
from django.utils.translation import ugettext_lazy as _

def textual(title, ordering_field=None):
    """
    Fallbacks textual field to '---' instead of (None) in admin.
    
    Sets proper title using ``title`` and if specified also ``admin_order_field``
    using ``ordering_field`` attribute.
    """
    def decorator(func):
        def wraps(self, obj):
            result = func(self, obj)
            return result if result else u'---'

        wraps.short_description = title
        wraps.allow_tags = True

        if ordering_field:
            wraps.admin_order_field = ordering_field

        return wraps
    return decorator


class BorisBaseAdmin(ModelAdmin):
    """
    Adds ``list_actions`` to simplify addition of actions to changelist rows. 
    """
    list_actions = ('change_link',)

    def __init__(self, *args, **kwargs):
        self.list_display += ('actions_display',)
        super(BorisBaseAdmin, self).__init__(*args, **kwargs)

    def actions_display(self, obj):
        return ''.join(getattr(self, a)(obj) for a in self.list_actions)
    actions_display.allow_tags = True
    actions_display.short_description = _(u'Akce')

    def change_link(self, obj):
        return u'<a href="%s" class="changelink cbutton">%s</button>' % (
            obj.get_admin_url(), _('upravit'))
