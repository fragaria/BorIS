from django import template
from django.template import loader

register = template.Library()


@register.simple_tag(takes_context=True)
def render_tab_form(context, tab, form):
    t = loader.get_template(tab.template)
    return t.render({'tab': tab, 'form': form})
