from django.utils.translation import gettext as _, LANGUAGE_SESSION_KEY, get_language_from_request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .forms import AddAuthorForm, EditBookForm
from posts.models import Post
import json
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg


# Create your views here.


def books(request):
    genres = Genres.objects.all()
    all_books = get_query(request)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_books, 16)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {'title': 'Browser books, Spimebook',
               'books': books, 'genres': genres}
    return render(request, 'books/index.html', context)


def book(request, book_id):
    lang = get_lang(request)
    target_book = get_object_or_404(Book, id=book_id).translate(lang)
    readed_book_state = False
    rating = target_book.book.rating_set.all().aggregate(Avg('rating'))
    if request.user.is_authenticated:
        user = request.user.profile
        if user.books.filter(id=target_book.book.id).exists():  # cheek:
            readed_book_state = True
        else:
            readed_book_state = False
    all_posts = Post.objects.filter(
        for_book=target_book.book).filter(archived=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'title': target_book.title + _(', Spimebook'),
               'book': target_book,
               'posts': posts,
               'readed_book': readed_book_state,
               'rating': rating
               }
    return render(request, 'books/book.html', context)


def search_book(request):
    if request.is_ajax():
        lang = get_lang(request)
        a = request.GET.get('term', '')
        objects = get_query(request)
        # titles = objects.filter(title__istartswith=a)
        titles = objects.filter(title__contains=a)
        print(titles)
        result = []
        data = ''
        for n in titles:
            author = eval(f'n.book.author.{lang}')
            result.append(n.title + f', {author}')
            data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def genres(request, genre):
    genre_id = Genres.objects.get(genre=genre).id
    books = get_query(request).filter(book__genres=genre_id)
    genres = Genres.objects.all()
    context = {'title': f'Browser {genre} books, Spimebook',
               'books': books, 'genres': genres}
    return render(request, 'books/index.html', context)


def add_genre(request, genre):
    mimetype = 'application/json'
    if request.method == 'POST':
        value = request.POST['name']
        genre = Genres(genre=value)
        native_lang = request.user.profile.lang
        for lang in settings.SUPPORTED_LANGS:
            lang = lang.lower()
            if lang.lower() == native_lang:
                exec(f"genre.genre_{lang} = '{value}'")
            translate_value = translator.translate(
                value, dest=lang, src=native_lang).text
            exec(f"genre.genre_{lang} = '{translate_value}'")
        genre.genre = genre.genre_en
        genre.save()
        data = {
            'state': str(type(genre)),
        }
        data = json.dumps(data)
        return HttpResponse(data, mimetype)
    return JsonResponse({'state': False})


def book_by_ajax(request, book_title_author):
    title = book_title_author.split(', ')[0]
    book = get_query(request).get(title__istartswith=title)
    return redirect(f'/books/{book.id}/')


@login_required(login_url='log-in')
def add_book(request):
    lang = get_lang(request)
    genres = Genres.objects.all()
    if request.method == 'POST':
        author = request.POST['author']
        exec(f'from authors.models import {lang.upper()} as Author')
        if not eval(f"Author.objects.filter(name='{author}').exists()"):
            messages.add_message(
                request, messages.ERROR, _('Author not found, please correct name or add to database.'))
        else:
            aut = eval(f"Author.objects.get(name=author)")
            title = request.POST['title']
            pub_date = request.POST['pub_date']
            bio = request.POST['book_Bio']
            b_type = request.POST['b_type']
            genres = request.POST.getlist('category')
            FILES = dict(request.FILES)
            author = aut.author
            english_title = translator.translate(title).text
            if FILES.__contains__('image'):
                image = FILES['image'][0]
                book = Book(title=english_title, book_image=image,
                            author=author, publish_date=pub_date, book_or_Novel=b_type)
            else:
                book = Book(title=english_title, author=author,
                            publish_date=pub_date, book_or_Novel=b_type)
            book.save()
            for g in genres:
                g = get_object_or_404(Genres, genre=g)
                book.genres.add(g)
            book.save()
            save_translate_for_all(lang, title, object=book)
            translate = eval(
                f"{lang.upper()}.objects.get(id=book.{lang}.id)")
            translate.title = title
            translate.book_Bio = bio
            translate.save()
            return redirect(f'/books/{book.id}')

    return render(request, 'books/add_book.html', {'title': 'Add Book', 'genres': genres})


'''
    if request.is_ajax():
        a = request.GET.get('term', '')
        names = Author.objects.filter(name__istartswith=a)
        result = []
        for n in names:
            name_json = n.author.name
            result.append(name_json)
            data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
'''


@login_required(login_url='log-in')
def edit_book(request, book_id):
    lang = get_lang(request)
    book = get_object_or_404(Book, id=book_id).translate(lang)
    form = EditBookForm(request.POST or None,
                        request.FILES or None, instance=book)
    genres = Genres.objects.all()
    if request.method == 'POST':
        form = EditBookForm(request.POST, request.FILES, instance=book.book)
        author = request.POST['author']
        exec(f'from authors.models import {lang.upper()} as Author')
        if not eval(f"Author.objects.filter(name='{author}').exists()"):
            messages.add_message(
                request, messages.ERROR, _('Author not found, please correct name or add to database.'))
        else:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                form.save_m2m()

                title = request.POST['title']
                b_type = request.POST['book_or_Novel']
                pub_date = request.POST['pub_date']
                bio = request.POST['book_Bio']
                genres = request.POST.getlist('category')

                book.title = title
                book.book_Bio = bio
                main_book = book.book
                main_book.book_or_Novel = b_type
                main_book.publish_date = pub_date
                book.save()
                main_book.genres.clear()

                for g in genres:
                    g = get_object_or_404(Genres, genre=g)
                    main_book.genres.add(g)

                main_book.save()

                return redirect(f'/books/{book_id}')
            else:
                form = EditBookForm(initial=request.POST)
                return render(request, 'books/edit_book.html', {'title': f'Edit {book.title} details', 'book': book, 'form': form})
    context = {
        'title': f'Edit {book.title} details',
        'book': book,
        'form': form,
        'genres': genres
    }
    return render(request, 'books/edit_book.html', context)


@login_required(login_url='log-in')
def readed_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user.profile
    print(user)
    if user.books.filter(id=book.id).exists():  # cheek:
        book.books.remove(user)
        msg = f'{book.title} removed from readed list!'
        readed_book_state = False
    else:
        book.books.add(user)  # love
        msg = f'{book.title} add to readed list.'
        readed_book_state = True
    return JsonResponse({'msg': msg, 'readed_book': readed_book_state})


@login_required(login_url='log-in')
def rating_book(request, book_id, rating):
    book = Book.objects.get(id=book_id)
    user = request.user
    if Rating.objects.filter(book=book).filter(user=user).exists():
        rate = Rating.objects.filter(book=book).get(user=user)
        rate.rating = rating
        rate.save()
        msg = 'already'

    else:
        rate = Rating(book=book, user=user, rating=rating)
        rate.save()
        msg = 'Done'

    rating = book.rating_set.all().aggregate(Avg('rating'))
    #rating = round(rating.rating__avg, 2)
    ratings_num = len(book.rating_set.all())
    return JsonResponse({'msg': msg, 'rating': rating, 'ratings_num': ratings_num})


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
    translate = eval(f"{lang}.objects.all()")
    return translate


def save_translate_for_all(native_lang, text, object):
    book = object
    for lang in settings.SUPPORTED_LANGS:
        if lang.lower() == native_lang:
            continue
        auto_text = translator.translate(
            text=', Google translator', dest=lang).text
        translate = translator.translate(text, dest=lang, src=native_lang).text
        translated_object = eval(
            f"{lang.upper()}.objects.get(id=book.{lang.lower()}.id)")
        translated_object.title = translate + ', ' + auto_text
        translated_object.save()
