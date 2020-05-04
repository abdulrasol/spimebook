from django.utils.translation import gettext as _, LANGUAGE_SESSION_KEY, get_language_from_request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from books.models import Book
from googletrans import Translator
from django.conf import settings
from .models import *
import json

TITLE = _('Spimebook')

translator = Translator()


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
        'title': _('Authors, %(title)s') % {'title': TITLE},
        'authors': authors,
    }
    response = render(request, 'authors/index.html', context)
    return response


def author(request, author_id, author_name):
    lang = get_lang(request)
    target_author = get_object_or_404(Author, id=author_id).translate(lang)
    exec(f'from books.models import {lang.upper()} as Book_lang')
    books = eval(
        f"Book_lang.objects.filter(book__author='{target_author.author.id}')")
    title = _('%(author)s, %(title)s') % {
        'author': target_author.name, 'title': TITLE}
    context = {
        'title': title,
        'author': target_author,
        'books': books,
    }
    response = render(request, 'authors/author.html', context)
    return response


@login_required(login_url='log-in')
def add_author(request):
    lang = get_lang(request)
    if request.method == 'POST':
        lang = lang.upper()
        name = request.POST['name']
        english_name = translator.translate(name).text
        born_date = request.POST['born_date']
        short = request.POST['short']
        bio = request.POST['author_Bio']
        FILES = dict(request.FILES)
        if FILES.__contains__('Author_Image'):
            image = FILES['Author_Image'][0]
            author = Author(title=english_name, born_date=born_date,
                            Author_Image=image)
        else:
            author = Author(title=english_name, born_date=born_date)
        author.save()
        save_translate_for_all(lang, name, author)
        author.id
        trans_author = eval(f"{lang}.objects.get(id={author.id})")
        trans_author.name = name
        trans_author.author_Bio = bio
        trans_author.short = short
        trans_author.save()
        return redirect(f'/authors/{author.id}/{name}')
    else:
        pass
    title = _('Add Author, %(title)s') % {'title': TITLE}
    return render(request, 'authors/add.html', {'title': title})


@login_required(login_url='log-in')
def edit_author(request, author_id, author_name):
    lang = get_lang(request)
    author = get_object_or_404(Author, id=author_id)
    translate = author.translate(lang)
    if author.translate(lang).name is None:
        author.translate(lang).name = translator.translate(
            author.title, dest=lang).text
        author.translate(lang).save()
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
        author.translate(lang).name = name
        author.translate(lang).author_Bio = bio
        author.translate(lang).short = short
        author.save()
        author.translate(lang).save()
        return redirect(f'/authors/{author.id}/{name}')
    title = _('Edit %(t)s details, %(title)s') % {
        't': translate.name, 'title': TITLE}
    context = {
        'title': title,
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


def get_query(request):
    if request.user.is_authenticated:
        lang = request.user.profile.lang
    else:
        lang = get_language_from_request(request)
        for tu in settings.LANGUAGES:
            if lang in tu:
                break
            else:
                lang = 'en'
    lang = lang.upper()
    translate = eval(f"({lang}.objects.all()")
    return translate


def save_translate_for_all(native_lang, text, object):
    author = object
    for lang in settings.SUPPORTED_LANGS:
        if lang.lower() == native_lang:
            continue
        translate = translator.translate(text, dest=lang, src=native_lang).text + \
            ', ' + \
            translator.translate(text='Google translator', dest=lang).text
        translated_object = eval(f"{lang}.objects.get(id={author.id})")
        translated_object.name = translate
        translated_object.save()
