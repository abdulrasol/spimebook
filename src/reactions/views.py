from django.shortcuts import render
from posts.models import Post
from django.shortcuts import get_object_or_404
from .models import Love, Comment
from books.models import Book
from django.contrib.auth.decorators import login_required
from django_ajax.decorators import ajax
import json
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
'''
send_mail('Subject here','Here is the message.','spimebook@gmail.com',[
          'iraq.rsol@gmai.com'],fail_silently=False)
'''
@ajax
@login_required(login_url='log-in')
def get_all_books(request):
    lang = request.user.profile.lang.upper()
    books = eval(f'{lang}.objects.all()')
    data = []
    for book in books:
        book_info = {
            'book': book.book,
            'id': book.id,
            'title': book.title
        }
        data.append(book_info)
    return data


@ajax
@login_required(login_url='log-in')
def new_post(request, book_id):
    user = request.user
    lang = user.profile.lang
    content = request.POST['content']
    p_type = request.POST['p_type']
    if request.POST['type'] == 'bookpost':
        book = get_object_or_404(Book, id=book_id)
        if p_type == 'Q':
            title = f'Quotes for {book.title}'
        else:
            title = f'Review for {book.title}'
        post = Post(user=user, title=title, lang=lang,
                    content=content, post_type=p_type, for_book=book)
        post.save()
        context = {
            'id': book.id,
            'type': 'book'
        }
    else:
        title = request.POST['title']
        post = Post(user=user, title=title, lang=lang,
                    content=content, post_type=p_type)
        if 'book' in request.POST:
            print(request.POST['book'])
            book = get_object_or_404(Book, id=request.POST['book'])
            post.for_book = book
        post.save()
        context = {
            'id': post.id,
            'type': 'post'
        }
    return context


@ajax
@login_required(login_url='log-in')
def add_commnet(request, post_id):
    post_type = request.POST['post_type']
    print(post_type)
    if post_type == 'book':
        post = Post.objects.get(id=post_id)
    else:
        post = Post.objects.get(id=post_id)

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


@ajax
@login_required(login_url='log-in')
def love(request, post_id):
    post_type = request.GET['type']
    if post_type == 'book':
        post = Post.objects.get(id=post_id)
    else:
        post = Post.objects.get(id=post_id)
    user = request.user
    if post.loves.filter(user=user).exists():  # cheek:
        loves = post.loves.get(user=user)
        loves.delete()
        msg = f'unlove'
        love = False
    else:
        loves = Love(post=post, user=user)
        loves.save()
        msg = f'love'
        love = True
    return {'msg': msg, 'love': love}


@ajax
def send_email(request):
    data = {
        'name': 'AbdulRasol',
        'mail': 'spimebook@gmail.com',
    }
    html_message = render_to_string('reactions/mail.html', context=data)
    plan_text = strip_tags(html_message)

    send_mail('Subject', plan_text, 'spimebook@gmail.com', [
              'iraq.rsol@gmail.com', 'abdulrsol97@gmail.com'], fail_silently=False, html_message=html_message)
    return 'ok'
