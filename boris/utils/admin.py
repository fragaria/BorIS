'''
Created on 12.2.2012

@author: xaralis
'''
from django.contrib.admin.options import ModelAdmin, csrf_protect_m
from django.contrib.admin.views.main import ChangeList
from django.db import transaction
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


class BorisChangeList(ChangeList):
    """Change list_display with respect to request."""

    remove_in_popup = ('actions_display',)

    def __init__(self, request, *args, **kwargs):
        super(BorisChangeList, self).__init__(request, *args, **kwargs)

        # Display different buttons based on whether we render a pop-up window.
        if 'pop' in request.GET:
            self.list_display.insert(0, 'select_link')
            self.list_display = filter(lambda x: x not in self.remove_in_popup,
                self.list_display)


class BorisBaseAdmin(ModelAdmin):
    """
    Adds ``list_actions`` to simplify addition of actions to changelist rows.
    """
    list_actions = ('change_link',)

    def __init__(self, *args, **kwargs):
        self.list_display += ('actions_display',)
        super(BorisBaseAdmin, self).__init__(*args, **kwargs)

    def get_changelist(self, request, **kwargs):
        return BorisChangeList

    def actions_display(self, obj):
        return ''.join(getattr(self, a)(obj) for a in self.list_actions)
    actions_display.allow_tags = True
    actions_display.short_description = _(u'Akce')

    def change_link(self, obj):
        return u'<a href="%s" class="changelink cbutton">%s</button>' % (
            obj.get_admin_url(), _('upravit'))

    def select_link(self, obj):
        return u'<a href="%s" ' \
                   'class="changelink cbutton" ' \
                   'onclick="opener.dismissRelatedLookupPopup(window, \'%s\');' \
                            'return false;"' \
                '>%s</button>' % (
            '%s/' % obj.pk, obj.pk, _('vybrat'))
    select_link.allow_tags = True
    select_link.short_description = ''

    def show_save(self, obj):
        return False

    def show_save_as_new(self, obj):
        return False

    def show_save_and_continue(self, obj):
        return True

    def show_save_and_add_another(self, obj):
        return False

    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        buttons_context = {
            'BO_SHOW_SAVE': self.show_save(obj),
            'BO_SHOW_SAVE_AS_NEW': self.show_save_as_new(obj),
            'BO_SHOW_SAVE_AND_CONT': self.show_save_and_continue(obj),
            'BO_SHOW_SAVE_AND_ADD_ANOTHER': self.show_save_and_add_another(obj)
        }
        if extra_context is not None:
            extra_context.update(buttons_context)
        else:
            extra_context = buttons_context
        return super(BorisBaseAdmin, self).change_view(request, object_id,
            extra_context)

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        buttons_context = {
            'BO_SHOW_SAVE': self.show_save(self.model()),
            'BO_SHOW_SAVE_AS_NEW': self.show_save_as_new(self.model()),
            'BO_SHOW_SAVE_AND_CONT': self.show_save_and_continue(self.model()),
            'BO_SHOW_SAVE_AND_ADD_ANOTHER': self.show_save_and_add_another(
                self.model())
        }
        if extra_context is not None:
            extra_context.update(buttons_context)
        else:
            extra_context = buttons_context
        return super(BorisBaseAdmin, self).add_view(request, form_url,
            extra_context)
