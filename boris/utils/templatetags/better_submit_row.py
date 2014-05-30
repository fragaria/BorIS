'''
Created on 24.3.2012

@author: xaralis
'''
from django import template

register = template.Library()


def orig_submit_row(context):
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and (change or ('show_delete' in context and context['show_delete']))),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True
    }


def get_captions(context):
    """Extract captions from context and map them to more readable names."""
    caption_keys = (
        ('BO_SAVE_CAPTION', 'save_caption'),
        ('BO_SAVE_AS_NEW_CAPTION', 'save_as_new_caption'),
        ('BO_SAVE_AND_CONT_CAPTION', 'save_and_cont_caption'),
        ('BO_SAVE_AND_ADD_ANOTHER_CAPTION', 'save_and_add_another_caption'),
        ('BO_DELETE_CAPTION', 'delete_caption'),
    )
    captions = {}
    for old_key, new_key in caption_keys:
        captions[new_key] = context.get(old_key, '')
    return captions


def submit_row(context):
    """
    Displays the row of buttons for delete and save. Uses enhanced rules that
    can be defined in administration class and passed through context.
    """
    data = orig_submit_row(context)

    if 'BO_SHOW_SAVE' in context:
        data['show_save'] = (context['BO_SHOW_SAVE'] and data['show_save'])

    if 'BO_SHOW_SAVE_AS_NEW' in context:
        data['show_save_as_new'] = (context['BO_SHOW_SAVE_AS_NEW'] and
                                    data['show_save_as_new'])

    if 'BO_SHOW_SAVE_AND_ADD_ANOTHER' in context:
        data['show_save_and_add_another'] = (
            context['BO_SHOW_SAVE_AND_ADD_ANOTHER'] and
            data['show_save_and_add_another'])

    if 'BO_SHOW_SAVE_AND_CONT' in context:
        data['show_save_and_continue'] = context['BO_SHOW_SAVE_AND_CONT']

    if context.get('BO_FORCE_SHOW_DELETE', False) is True:
        data['show_delete_link'] = True

    data.update(get_captions(context))

    return data

submit_row = register.inclusion_tag('admin/submit_line.html', takes_context=True)(submit_row)
