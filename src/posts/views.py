from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden, HttpResponse
from .models import Post, Comment
from .forms import AddCommentForm, EditPostForm
from books.models import Author, Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg
from django.utils.translation import gettext as _
from django_ajax.decorators import ajax


# Create your views here.


def test(request):
    all_posts = range(1, 1000)
    top_ten_books = Book.objects.filter(book_or_Novel='Book').annotate(
        readed=Count('books')).order_by('-readed')[:10]
    top_ten_movels = Book.objects.filter(book_or_Novel='Novel').annotate(
        readed=Count('books')).order_by('-readed')[:10]
    top_rate = Book.objects.order_by('-rating')[:10]
    # rating = book.rating_set.all().aggregate(Avg('rating'))
    print(top_rate)
    # print(top10[0].books_count)
    all_posts = Post.objects.filter(
        archived=False).annotate(loves_count=Count('comments')).order_by('-loves_count')
    # uestion.objects.filter(date__gt=datetime.now() - timedelta(hours=1)).annotate(num_votes=Count('has_voted')).order_by('-num_votes')

    return render(request, 'posts/test.html', {'books': top_ten_books, 'novels': top_ten_movels, 'top_rate': top_rate, 'posts': all_posts})


def home(request):
    comment_form = AddCommentForm()
    all_posts = Post.objects.filter(archived=False)
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
    context = {
        'title': target_post.title,
        'post': target_post,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post.html', context)


@login_required(login_url='log-in')
def new_post(request):
    if request.method == 'POST':
        book = request.POST['for_book']
        book = book.split(', ')[0]
        lang = request.user.profile.lang.upper()
        exec(f'from books.models import {lang} as book_{lang}')
        if not eval(f"book_{lang}.objects.filter(title='{book}').exists()"):
            messages.add_message(
                request, messages.ERROR, _('Book not found, please correct title or add to database.'))
        else:
            title = request.POST['title']
            content = request.POST['content']
            p_type = request.POST['p_type']
            # get book for this post
            book = get_book(request, book)
            print(book)
        # print(f'title: {book_title} for {book_author}, {target_book}')
            post = Post(user=request.user, title=title,
                        content=content, post_type=p_type, for_book=book.book)
            post.save()
            return redirect(f'/post/{post.id}')

    return render(request, 'posts/new_post.html', {'title': 'New Post'})


@login_required(login_url='log-in')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not request.user == post.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        # get book for this post
        book = request.POST['for_book']
        book = book.split(', ')[0]
        lang = request.user.profile.lang.upper()
        exec(f'from books.models import {lang} as book_{lang}')
        if not eval(f"book_{lang}.objects.filter(title='{book}').exists()"):
            messages.add_message(
                request, messages.ERROR, _('Book title incorrect, please correct title or add to database.'))
        else:
            book = request.POST['for_book']
            book = book.split(', ')[0]
            book = get_book(request, book)
            title = request.POST['title']
            content = request.POST['content']
            p_type = request.POST['post_type']

            post.for_book = book.book

            post.title = title
            post.content = content
            post.post_type = p_type

            archived = request.POST.getlist('archiving')
            if not (not archived):
                post.archived = True
            else:
                post.archived = False
            post.save()
            return redirect(f'/post/{post.id}')

    return render(request, 'posts/edit_post.html', {'title': f'Edit {post.title}', 'post': post})


@login_required(login_url='log-in')
def my_posts(request, user):
    all_posts = Post.objects.filter(user=request.user)
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
        'title': 'My posts, Spimebook',
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/my_posts.html', context)


'''
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
'''


@ajax
@login_required(login_url='log-in')
def add_commnet(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment = request.POST['comment']
        comment = Comment(user=request.user, comment=comment, post=post)
        comment.save()
        img = request.user.profile.picture.url
        context = {
            'comment': comment.comment,
            'img': img,
            'user': request.user,
            'time': comment.comment_date.strftime("%d %b %Y, %H:%M"),
        }
    return context


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


def get_book(requset, title):
    lang = requset.user.profile.lang
    lang = lang.upper()
    exec(f'from books.models import {lang} as book_{lang}')
    if eval(f"book_{lang}.objects.get(title='{title}')"):
        book = eval(f"get_object_or_404(book_{lang}, title = '{title}')")

    return book
