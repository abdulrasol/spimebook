from django.utils.translation import gettext as _, LANGUAGE_SESSION_KEY, get_language_from_request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *


import json
from django.conf import settings

# Create your views here.


def authors(request):
    lang = get_lang(request)
    authors_list = eval(f"{lang.upper()}.objects.all()")

    page = request.GET.get('page', 1)
    paginator = Paginator(authors_list, 20)

    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    context = {
        'title': _('Authors, Spimebook'),
        'authors': authors,
    }
    response = render(request, 'authors/index.html', context)
    return response


def author(request, author_id, author_name):
    lang = get_lang(request)
    target_author = eval(f"{lang.upper()}.objects.get(id={author_id})")
    # print(str(target_author))
    context = {
        'title': f'{target_author}, Spimebook',
        'author': target_author,
    }
    response = render(request, 'authors/author.html', context)
    return response


@login_required(login_url='log-in')
def add_author(request):
    if request.method == 'POST':
        lang = request.user.profile.lang.upper()
        name = request.POST['name']
        born_date = request.POST['born_date']
        short = request.POST['short']
        bio = request.POST['author_Bio']
        FILES = dict(request.FILES)
        if FILES.__contains__('Author_Image'):
            image = FILES['Author_Image'][0]
            author = Author(title=name, born_date=born_date,
                            Author_Image=image)
        else:
            author = Author(title=name, born_date=born_date)
        author.save()
        trans_author = eval(f"{lang}.objects.get(id={author.id})")
        trans_author.name = name
        trans_author.author_Bio = bio
        trans_author.short = short
        trans_author.save()
        return redirect(f'auth/a/{author.id}/{name}')
    else:
        pass
    title = _('Add Author, Spimebook')
    return render(request, 'authors/add.html', {'title': title})


@login_required(login_url='log-in')
def edit_author(request, author_id, author_name):
    lang = get_lang(request)
    author = get_object_or_404(Author, id=author_id)
    translate = eval(f"get_object_or_404({lang.upper()}, id = {author_id})")
    print(translate, author)
    if request.method == 'POST':
        lang = request.user.profile.lang.upper()
        name = request.POST['name']
        born_date = request.POST['born_date']
        short = request.POST['short']
        bio = request.POST['author_Bio']
        FILES = dict(request.FILES)
        if FILES.__contains__('Author_Image'):
            image = FILES['Author_Image'][0]
            author.Author_Image = image

        author.born_date = born_date
        author.save()

        translate.name = name
        translate.author_Bio = bio
        translate.short = short
        translate.save()
        return redirect(f'/author/{author.id}/{name}')
    context = {
        'title': f'Edit {translate} details, Spimebook',
        'author': translate,
    }
    return render(request, 'authors/edit.html', context)


def author_autocomplete(request):
    lang = get_lang(request).upper()
    if request.is_ajax():
        a = request.GET.get('term', '')
        Query = eval(f'{lang}.objects.all()')
        names = Query.filter(name__istartswith=a)
        result = []
        data = None
        for n in names:
            name_json = n.name
            result.append(name_json)
            data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_lang(request):
    if request.user.is_authenticated:
        lang = request.user.profile.lang
    else:
        lang = get_language_from_request(request)
        for tu in settings.LANGUAGES:
            if lang in tu:
                break
            else:
                lang = 'en'
    return lang


def get_trans(request):
    if request.user.is_authenticated:
        lang = request.user.profile.lang
        lang = lang.upper()
        print(lang)
        translate = eval(f"({lang}()")
        print(translate)
    else:
        lang = get_language_from_request(request)
        for tu in settings.LANGUAGES:
            if lang in tu:
                break
            else:
                lang = 'en'
            translate = eval(f"({lang.upper()}()")
    return translate
