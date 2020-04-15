from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from .models import Post, Comment
from .forms import AddCommentForm

# Create your views here.


def home(request):
    posts = Post.objects.all()
    comment_form = AddCommentForm()
    if request.user.is_authenticated:
        print('is_authenticated')
    else:
        print('not_authenticated')
    context = {
        'title': 'Spimebook, a site for readers',
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/index.html', context)


def post(request, post_id):
    target_post = Post.objects.get(id=post_id)
    comment_form = AddCommentForm()
    if request.user.is_authenticated:
        print('is_authenticated')
    else:
        print('not_authenticated')
    context = {
        'post': target_post,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post.html', context)


@login_required(login_url='log-in')
def my_post(request, user):
    posts = Post.objects.filter(user=request.user)
    comment_form = AddCommentForm()

    context = {
        'title': 'Spimebook, a site for readers',
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/my_post.html', context)


def add_comment(request, post_id):
    target_post = Post.objects.get(id=post_id)
    #    comment_form = AddCommentForm()
    context = {
        'post': target_post,
        'comment': target_post,
    }
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddCommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            get_comment = form.cleaned_data['comment']
            save_comment = Comment(
                user=request.user, comment=get_comment, post=target_post)
            save_comment.save()
            # target_comment = save_comment
            # redirect to a new URL:
            return render(request, 'posts/post.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponseRedirect('/')
    return render(request, 'posts/post.html', context)


@login_required(login_url='log-in')
def love(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user.profile
    print(user)
    #  u1.saves.filter(id = 2).exists()
    if user.loves.filter(id=post.id).exists():  # cheek:
        post.loves.remove(user)
        msg = f'unlove {post.title}'
        love = False
    else:
        post.loves.add(user)  # love
        msg = f'love {post.title}'
        love = True
    return JsonResponse({'msg': msg, 'love': love})


@login_required(login_url='log-in')
def save(request, post_id):
    post = Post.objects.get(id=post_id)
    print(post)
    user = request.user
    saves = list(user.profile.saves.all())
    if saves.__contains__(user):
        user.profile.saves.remove(post)
        messages.add_message(request, messages.SUCCESS,
                             f'{post.title} removed from saved list ')
    else:
        user.profile.saves.add(post)
        messages.add_message(request, messages.SUCCESS,
                             f'{post.title} adden to saved list ')

    context = {
        'post': post,
    }
    # print(user)
    # print(post)
    # post = Post.objects.get(id=post_id)
    # print(post)
    return render(request, 'posts/post.html', context)
