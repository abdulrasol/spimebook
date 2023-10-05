from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden, HttpResponse
from .models import Post
from reactions.models import Comment
from books.models import Author, Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg
from django.utils.translation import gettext as _
from django_ajax.decorators import ajax
from books.views import get_query


# Create your views here.
TITLE = _('Spimebook')


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
    all_posts = Post.objects.filter(archived=False).filter(post_type='P')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 7)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'title': _('Spimebook, a site for readers'),
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def quotes(request):
    all_posts = Post.objects.filter(post_type='Q').filter(archived=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 7)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'title': _('Spimebook, a site for readers'),
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def post(request, post_id):
    target_post = Post.objects.get(id=post_id)
    context = {
        'title': _('%(post)s, %(title)s') % {'post': target_post.title, 'title': TITLE},
        'post': target_post,
    }
    return render(request, 'posts/post.html', context)


@login_required(login_url='log-in')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not request.user == post.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        p_type = request.POST['post_type']
        archived = request.POST.getlist('archiving')
        if 'for_book' in request.POST:
            book = get_object_or_404(Book, id=request.POST['for_book'])
            post.for_book = book
        post.title = title
        post.content = content
        post.post_type = p_type
        if not (not archived):
            post.archived = True
        else:
            post.archived = False
        post.save()
        return redirect(f'/posts/post/{post.id}/')
    context = {
        'title': _('Edit %(title)s' % {'title': post.title}),
        'post': post,
        'books': Book.objects.all()
    }
    return render(request, 'posts/edit_post.html', context=context)


@login_required(login_url='log-in')
def my_posts(request, user):
    all_posts = Post.objects.filter(user=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 7)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'title': _('My Posts, Spimebook'),
        'posts': posts,
    }
    return render(request, 'posts/my_posts.html', context)


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
    return render(request, 'posts/post.html', context)
