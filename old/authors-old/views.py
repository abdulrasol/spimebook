from django.utils.translation import gettext as _, LANGUAGE_SESSION_KEY, get_language_from_request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from books.models import Book

from django.conf import settings
from .models import *
import json

TITLE = _('Spimebook')



def authors(request):
    authors_list = Author.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(authors_list, 20)
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)
    context = {
        'title': _('Authors, %(title)s') % {'title': TITLE},
        'authors': authors,
    }
    response = render(request, 'authors/index.html', context)
    return response


def author(request, author_id, author_name):
    author = get_object_or_404(Author, id=author_id)
    books = author.book_set.all()
    title = _('%(author)s, %(title)s') % {
        'author': author.name, 'title': TITLE}
    context = {
        'title': title,
        'author': author,
        'books': books,
    }
    response = render(request, 'authors/author.html', context)
    return response


@login_required(login_url='log-in')
def add_author(request):
    if request.method == 'POST':
        name = request.POST['name']
        born_date = request.POST['born_date']
        short = request.POST['short']
        bio = request.POST['author_Bio']
        FILES = dict(request.FILES)
        if FILES.__contains__('Author_Image'):
            image = FILES['Author_Image'][0]
            author = Author(name=name, born_date=born_date,
                            Author_Image=image)
        else:
            author = Author(name=english_name, born_date=born_date)
        author.save()
        return redirect(f'/authors/{author.id}/{name}')
    else:
        pass
    title = _('Add Author, %(title)s') % {'title': TITLE}
    return render(request, 'authors/add.html', {'title': title})


@login_required(login_url='log-in')
def edit_author(request, author_id, author_name):
    
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        
        author.name = request.POST['name']
        author.born_date = request.POST['born_date']
        author.short = request.POST['short']
        author.author_Bio = request.POST['author_Bio']
        print(request.POST['born_date'])
        FILES = dict(request.FILES)
        if FILES.__contains__('Author_Image'):
            image = FILES['Author_Image'][0]
            author.Author_Image = image
        author.save()
        return redirect(f'/authors/{author.id}/{author.name}')
    title = _('Edit %(t)s details, %(title)s') % {
        't': author.name, 'title': TITLE}
    context = {
        'title': title,
        'author': author,
    }
    return render(request, 'authors/edit.html', context)


def author_autocomplete(request):
    
    if request.is_ajax():
        a = request.GET.get('term', '')
        Query =Author.objects.all()
        names = Query.filter(name__istartswith=a)
        result = []
        data = None
        for n in names:
            name_json = n.name
            result.append(name_json)
            data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

