from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import Book, Author, Genres
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .forms import AddAuthorForm, EditBookForm
from posts.models import Post
import json

# Create your views here.


def books(request):
    books = Book.objects.all()
    genres = Genres.objects.all()
    context = {'title': 'Browser books, Spimebook',
               'books': books, 'genres': genres}
    return render(request, 'books/index.html', context)


def search_book(request):
    if request.is_ajax():
        '''
        query = request.GET.get("term", "")
        titles = Book.objects.filter(title__istartswith=query)
        ids = Book.objects.filter(title__istartswith=query)
        results = list(titles) + list(ids)
        data = json.dumps(results)
    else:
        data = 'fail'
    return HttpResponse(data, 'application/json')
    '''
        a = request.GET.get('term', '')
        titles = Book.objects.filter(title__istartswith=a)
        result = []
        data = ''
        for n in titles:
            result.append(n.title + f', {n.author}')
            data = json.dumps(result)

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def genres(request, genre):
    genre_id = Genres.objects.get(genre=genre).id
    books = Book.objects.filter(genres=genre_id)
    genres = Genres.objects.all()
    context = {'title': f'Browser {genre} books, Spimebook',
               'books': books, 'genres': genres}
    return render(request, 'books/index.html', context)


def book(request, book_id):
    target_book = get_object_or_404(Book, id=book_id)
    posts = Post.objects.filter(for_book=target_book)
    readed_book_state = False
    if request.user.is_authenticated:
        user = request.user.profile
        # print(user)
        if user.books.filter(id=target_book.id).exists():  # cheek:
            # target_book.books.remove(user)
            readed_book_state = True
        else:
            # target_book.books.add(user)  # love
            readed_book_state = False

    context = {'title': target_book.title,
               'book': target_book,
               'posts': posts,
               'readed_book': readed_book_state
               }
    # print(target_book.genres.all())
    return render(request, 'books/book.html', context)


def book_by_ajax(request, book_title_author):
    # print(book_title_author)
    book_title = book_title_author.split(', ')[0]
    # print(book_title)
    book_author = get_object_or_404(
        Author, author_Name=book_title_author.split(', ')[1])
    target_book = Book.objects.filter(
        title__icontains=book_title).get(author=book_author)
    # print(target_book)
    readed_book_state = False
    if request.user.is_authenticated:
        user = request.user.profile
        # print(user)
        if user.books.filter(id=target_book.id).exists():  # cheek:
            # target_book.books.remove(user)
            readed_book_state = True

    context = {'title': target_book.title,
               'book': target_book,
               'readed_book': readed_book_state
               }
    return render(request, 'books/book.html', context)


@login_required(login_url='log-in')
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        pub_date = request.POST['pub_date']
        b_type = request.POST['b_type']
        author = request.POST['author']
        bio = request.POST['bio']
        if not Author.objects.filter(author_Name=author).exists():
            messages.add_message(
                request, messages.ERROR, 'Author not found, kindly correct name or add to database')

        else:
            FILES = dict(request.FILES)
            author = Author.objects.get(author_Name=author)
            if FILES.__contains__('image'):
                image = FILES['image'][0]
                book = Book(title=title, book_image=image,
                            author=author, publish_date=pub_date, book_Bio=bio, book_or_Novel=b_type)
            else:
                book = Book(title=title, author=author,
                            publish_date=pub_date, book_Bio=bio, book_or_Novel=b_type)

            book.save()
            # print(book.id)
            return redirect(f'/books/{book.id}')

    return render(request, 'books/add_book.html', {'title': 'Add Book'})


@login_required(login_url='log-in')
def author_autocomplete(request):
    if request.is_ajax():
        a = request.GET.get('term', '')
        names = Author.objects.filter(author_Name__istartswith=a)
        result = []
        for n in names:
            name_json = n.author_Name
            result.append(name_json)
            data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required(login_url='log-in')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = EditBookForm(request.POST or None,
                        request.FILES or None, instance=book)
    if request.method == 'POST':
        form = EditBookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(
                request, messages.ERROR, f'{book.title} Saved, ')
            return redirect(f'/books/{book_id}')
        else:
            form = EditBookForm(initial=request.POST)
            return render(request, 'books/edit_book.html', {'title': f'Edit {book.title} details', 'book': book, 'form': form})

    return render(request, 'books/edit_book.html', {'title': f'Edit {book.title} details', 'book': book, 'form': form})


@login_required(login_url='log-in')
def readed_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user.profile
    print(user)
    #  u1.saves.filter(id = 2).exists()
    if user.books.filter(id=book.id).exists():  # cheek:
        book.books.remove(user)
        msg = f'{book.title} removed from readed list!'
        readed_book_state = False
    else:
        book.books.add(user)  # love
        msg = f'{book.title} add to readed list.'
        readed_book_state = True
    return JsonResponse({'msg': msg, 'readed_book': readed_book_state})


def author(request, author_id, book_author):
    author = get_object_or_404(Author, id=author_id)
    books = Book.objects.filter(author=author)
    # print(books)
    context = {'title': author.author_Name,
               'author': author,
               'books': books
               }
    return render(request, 'books/author.html', context)


@login_required(login_url='log-in')
def add_author(request):
    if request.method == 'POST':
        author = request.POST['author_Name']
        form = AddAuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.ERROR, f'{author} Added to database, ')
            return render(request, 'books/add_author.html', {'title': 'Add author', 'form': form})
        else:
            form = AddAuthorForm(initial=request.POST)
            return render(request, 'books/add_author.html', {'title': 'Add author', 'form': form})
    form = AddAuthorForm()
    return render(request, 'books/add_author.html', {'title': 'Add author', 'form': form})


@login_required(login_url='log-in')
def edit_author(request, author_id, author_name):
    author = get_object_or_404(Author, id=author_id)
    form = AddAuthorForm(request.POST or None,
                         request.FILES or None, instance=author)
    if request.method == 'POST':
        author_Name = author.author_Name
        form = AddAuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            print(type(instance))
            messages.add_message(
                request, messages.ERROR, f'{author_Name} Saved, ')
            return redirect(f'/authors/{author_id}/{author}')
        else:
            form = AddAuthorForm(initial=request.POST)
            return render(request, 'books/add_author.html', {'title': 'Add author', 'form': form})

    # form = AddAuthorForm(data=data)
    return render(request, 'books/edit_author.html', {'title': f'Edit {author.author_Name} details', 'author': author, 'form': form})
