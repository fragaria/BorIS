from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, *urls):
    path = context['request'].get_full_path()

    for url in urls:
        if (url == '/' or url == '') and not (path == '/' or path == ''):
            return ''
        if url and path.startswith(url):
            return 'active'
        return ''
