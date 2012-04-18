from django import template
from django.template import Node


register = template.Library()

class show_free(Node):
    def render(self, context):
        a = Article.objects.filter(status=1, articletype__slug='free-stuff').order_by('-pub_date')
        i = a[0].issueitems.all()[0].issue 
        context['show_free'] = a.filter(issueitems__issue=i)
        return ''

def get_show_free(parser, token):
    return show_free()

get_show_free = register.tag(get_show_free)




