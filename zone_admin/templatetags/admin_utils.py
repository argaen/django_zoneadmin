from django import template
register = template.Library()

@register.filter('input_type')
def input_type(ob):
    return ob.__class__.__name__

@register.filter(name='dir')
def showdir(field):
    print dir(field)
