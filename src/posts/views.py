from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from .models import Post, Comment
from .forms import AddCommentForm, EditPostForm
from books.models import Author, Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def test(request):
    numbers_list = range(1, 1000)

    page = request.GET.get('page', 1)

    paginator = Paginator(numbers_list, 20)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request, 'posts/test.html', {'numbers': numbers})


def home(request):

    all_posts = Post.objects.filter(archived=False)
    comment_form = AddCommentForm()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 7)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'title': 'Spimebook, a site for readers',
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/index.html', context)


def quotes(request):

    all_posts = Post.objects.filter(post_type='Q').filter(archived=False)
    comment_form = AddCommentForm()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 7)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
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
def new_post(request):

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        p_type = request.POST['p_type']
        for_book = request.POST['for_book']
        # get book for this post
        book_title = for_book.split(', ')[0]
        book_author = get_object_or_404(
            Author, author_Name=for_book.split(', ')[1])
        target_book = Book.objects.filter(
            title__icontains=book_title).get(author=book_author)
        #print(f'title: {book_title} for {book_author}, {target_book}')

        post = Post(user=request.user, title=title,
                    content=content, post_type=p_type, for_book=target_book)
        post.save()
        return redirect(f'/post/{post.id}')

    return render(request, 'posts/new_post.html', {'title': 'New Post'})


@login_required(login_url='log-in')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not request.user == post.user:
        return HttpResponseForbidden()
    form = EditPostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect(f'/post/{post_id}')
        else:
            form = EditPostForm(initial=request.POST)
            return render(request, 'posts/edit_post.html', {'title': f'Edit {post.title} details', 'book': book, 'form': form})

    return render(request, 'posts/edit_post.html', {'title': f'Edit {post.title}', 'post': post, 'form': form})


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
