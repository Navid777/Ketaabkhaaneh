from django import template
from bookreview.models import Image, Video

register = template.Library()

@register.inclusion_tag('tags/image.html')
def render_image(id, style, render_type):
    img = Image.objects.filter(id=id)
    if img.count() == 0:
        img = None
    else:
        img = img[0]
    return {
        'image': img,
        'style': style,
        'render_type': render_type,
    }

@register.inclusion_tag('tags/video.html')
def render_video(id, style, render_type):
    vid = Video.objects.filter(id=id)
    if vid.count() == 0:
        vid = None
    else:
        vid = vid[0]
    return {
        'video': vid,
        'style': style,
        'render_type': render_type,
    }
