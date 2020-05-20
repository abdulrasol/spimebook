from django import template


register = template.Library()


@register.filter(name='get_translate')
def get_translate(value, arg):
    if value == None:
        return None
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


@register.inclusion_tag('books/costumtags/post_container.html')
def book_post(post, user):
    context = {
        'user': user,
        'post': post
    }
    return context
