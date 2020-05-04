from django import template
from posts.models import Post, Comment
from posts.forms import AddCommentForm

register = template.Library()


@register.inclusion_tag('posts/costumtags/comment_form.html')
def comment_form(post_id):
    target_post = Post.objects.get(id=post_id)
    comment_form = AddCommentForm()
    context = {
        'post': target_post,
        'comment': target_post,
        'comment_form': comment_form,
    }
    return context


@register.inclusion_tag('posts/costumtags/reaction_bar.html')
def reaction_bar(post_id, user):
    target_post = Post.objects.get(id=post_id)
    comment_form = AddCommentForm()
    context = {
        'user': user,
        'post': target_post,
        'comment': target_post,
        'comment_form': comment_form,
    }
    return context


@register.inclusion_tag('posts/costumtags/post_container.html')
def post(post, user):
    context = {
        'user': user,
        'post': post
    }
    return context


@register.inclusion_tag('posts/costumtags/infinite_scroll_js.html')
def infinite_scroll_js():
    context = {
    }
    return context


@register.simple_tag
def love(user, post):
    if user.profile.loves.filter(id=post.id).exists():
        return True
    else:
        return False
