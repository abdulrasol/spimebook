from django.utils.translation import gettext as _, LANGUAGE_SESSION_KEY, get_language_from_request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Genres
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .forms import AddAuthorForm, EditBookForm
from posts.models import Post
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from django_ajax.decorators import ajax
from django.utils.translation import gettext as _
import json


# Create your views here.
TITLE = _('Spimebook')


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

    context = {
        'title': _('Browser books, %(title)s') % {'title': TITLE},
        'books': books, 'genres': genres
    }
    return render(request, 'books/index.html', context)


def book(request, book_id, posts='all'):
  
    target_book = get_object_or_404(Book, id=book_id)

    # check readed book or no ?
    readed_book_state = False
    if request.user.is_authenticated:
        user = request.user.profile
        if user.books.filter(id=target_book.book.id).exists():  # cheek:
            readed_book_state = True
        else:
            readed_book_state = False

    # Return posts [and Filterd]
    if posts == 'all':
        all_posts = Post.objects.filter(
            for_book=target_book.book).filter(archived=False)
        post_type = 'all'
    else:
        post_type = posts
        posts = posts[0].upper()
        all_posts = Post.objects.filter(
            for_book=target_book.book).filter(post_type=posts).filter(archived=False)
    # setup Paginators
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'title': target_book.title + ',' + TITLE,
        'book': target_book,
        'posts': posts,
        'readed_book': readed_book_state,
        'post_type': post_type
    }
    return render(request, 'books/book.html', context)


def search_book(request):
    if request.is_ajax():
        a = request.GET.get('term', '')
        objects = get_query(request)
        # titles = objects.filter(title__istartswith=a)
        titles = objects.filter(title__contains=a)
        # print(titles)
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
    genre = Genres.objects.get(genre=genre)
    context = {
        'title': _('Browser %(genre)s Books, ') % {'genre': genre} + TITLE,
        'books': books, 'genres': genres
    }
    return render(request, 'books/index.html', context)


# Book or Novel
def book_or_novel(request, book_type):
    books = get_query(request).filter(book__book_or_Novel=book_type)
    genres = Genres.objects.all()
    if book_type == 'Book':
        title = _('Browser Book') + ', ' + TITLE
    else:
        title = _('Browser Novel') + ', ' + TITLE
    context = {
        'title': title,
        'books': books, 'genres': genres
    }
    return render(request, 'books/index.html', context)


@ajax
@login_required(login_url='log-in')
def add_genre(request, genre):
    if request.method == 'POST':
        value = request.POST['name']
        genre = Genres(genre=value)
        genre.save()
    context = {
        'genre': genre
    }
    return context


def book_by_ajax(request, book_title_author):
    title = book_title_author.split(', ')[0]
    book = get_query(request).get(title__istartswith=title)
    return redirect(f'/books/{book.id}/')


@login_required(login_url='log-in')
def add_book(request):
    
    genres = Genres.objects.all()
    if request.method == 'POST':
        author = request.POST['author']
        from authors.models import  Author
        if not Author.objects.filter(name='{author}').exists():
            messages.add_message(
                request, messages.ERROR, _('Author not found, please correct name or add to database.'))
        else:
            aut = Author.objects.get(name=author)
            title = request.POST['title']
            pub_date = request.POST['pub_date']
            bio = request.POST['book_Bio']
            b_type = request.POST['b_type']
            genres_ids = request.POST.getlist('category')
            FILES = dict(request.FILES)
            author = aut.author
           
            if FILES.__contains__('image'):
                image = FILES['image'][0]
                book = Book(title=title, book_image=image,
                            author=author, publish_date=pub_date, book_or_Novel=b_type)
            else:
                book = Book(title=title, author=author,
                            publish_date=pub_date, book_or_Novel=b_type)
            book.save()
            for id in genres_ids:
                genre = get_object_or_404(Genres, id=id)
                book.genres.add(genre)

            book.save()
            return redirect(f'/books/{book.id}')
    context = {
        'title': _('Add Book'),
        'genres': genres
    }
    return render(request, 'books/add_book.html', context)


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
    book = get_object_or_404(Book, id=book_id).translate(lang)
    form = EditBookForm(request.POST or None,
                        request.FILES or None, instance=book)
    genres = Genres.objects.all()
    if request.method == 'POST':
        form = EditBookForm(request.POST, request.FILES, instance=book.book)
        author = request.POST['author']
        from authors.models import Author
        if not Author.objects.filter(name='{author}').exists():
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
                    g = get_object_or_404(Genres, id=g)
                    main_book.genres.add(g)

                main_book.save()

                return redirect(f'/books/{book_id}')
            else:
                form = EditBookForm(initial=request.POST)
                return render(request, 'books/edit_book.html', {'title': f'Edit {book.title} details', 'book': book, 'form': form})
    context = {
        'title': _('Edit') + ' ' + book.title,
        'book': book,
        'form': form,
        'genres': genres
    }
    return render(request, 'books/edit_book.html', context)


@login_required(login_url='log-in')
def readed_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user.profile
    # print(user)
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




def get_query(request):
    return Book.objects.all()

