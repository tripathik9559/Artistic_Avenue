from django import template
from django.templatetags.static import static

register = template.Library()

@register.filter
def pic_url(pic):
    """
    Returns correct URL for a pic field.
    - If pic starts with demo_arts/ or demo_artists/ → use {% static %}
    - Otherwise → use /media/ prefix
    """
    if not pic:
        return static('images/logo.png')
    pic_str = str(pic)
    if pic_str.startswith('demo_arts/') or pic_str.startswith('demo_artists/'):
        return static(pic_str)
    return f'/media/{pic_str}'
