from posts.models import Post
from django import template


register = template.Library()


@register.inclusion_tag('reactions/comment_form.html')
def comment_form(post_id):
    target_post = Post.objects.get(id=post_id)
    context = {
        'post': target_post,
    }
    return context


@register.inclusion_tag('reactions/reaction_bar_rev.html')
def reactions_bar_rev(post_id, user):
    target_post = Post.objects.get(id=post_id)
    context = {
        'user': user,
        'post': target_post,
    }
    return context


@register.inclusion_tag('reactions/reaction_bar_quo.html')
def reactions_bar_quo(post_id, user):
    target_post = Post.objects.get(id=post_id)
    context = {
        'user': user,
        'post': target_post,
    }
    return context
