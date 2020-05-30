from django.template.defaulttags import register

@register.filter('get_item')
def get_item(d, key):
    if key:
        return d.get(key)