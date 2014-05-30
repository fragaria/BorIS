'''
Created on 12.2.2012

@author: xaralis
'''
from django import template

register = template.Library()


@register.tag
def active(parser, token):
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return NavSelectedNode(args[1:])


class NavSelectedNode(template.Node):
    def __init__(self, urls):
        self.urls = urls

    def render(self, context):
        path = context['request'].path

        for url in self.urls:
            if '"' not in url:
                cpath = template.Variable(url).resolve(context)
            else:
                cpath = url.strip('"')

            if (cpath == '/' or cpath == '') and not (path == '/' or path == ''):
                return ""
            if cpath and path.startswith(cpath):
                return 'active'
        return ""
