from django import template
from posts.models import Post, Comment
from posts.forms import AddCommentForm

register = template.Library()


@register.filter(name='get_translate')
def get_translate(value, arg):
    translate = eval(f"value.{arg}")
    return translate


@register.filter(name='translate_genre')
def translate_genre(value, arg):
    translate = eval(f"value.genre_{arg}")
    return translate


@register.simple_tag
def define(val=None):
    # retrun the val
    return val
