from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from posts.models import Post
from .models import Profile
from .forms import EditProfileForm

# Create your views here.
# { % if user.is_authenticated % }


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 f'Welcome back {username} ')
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING,
                                 f'{username} not found')
            redirect('log-in')

    return render(request, 'users/login.html', {})


@login_required(login_url='log-in')
def log_out(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['username']).exists() or User.objects.filter(email=request.POST['email']).exists():
            messages.add_message(request, messages.SUCCESS,
                                 'username or email are taken')
            return redirect('register')

        else:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            # print(username, password, email)
            user = User.objects.create_user(username, email, password)
            user.save()
            #profile = Profile(user.id)
            # profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 f'Welcome {username}, your account created login now!')
            return redirect('log-in')

    return render(request, 'users/register.html', {'user_exists': False})


@login_required(login_url='log-in')
def profile(request):
    user = request.user
    print(request.user)
    posts = Post.objects.filter(user=user)
    readed_books = user.profile.books.all()
    if user.first_name == '':
        name = user.username
    else:
        name = user.first_name + ' ' + user.last_name
    context = {
        'title': f'{name} | Spimebook',
        'books': readed_books,
        'posts': posts,
    }

    return render(request, 'users/porfile.html', context)


@login_required(login_url='log-in')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        print(form)
    else:
        form = EditProfileForm()
    context = {
        'form': form
    }
    return render(request, 'users/edit_porfile.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    # print(f'userfrom url {username} and from db {user}')
    posts = Post.objects.filter(user=user)
    readed_books = user.profile.books.all()
    # print(books)
    # print(user.profile.picture.url)
    if user.first_name == '':
        name = user.username
    else:
        name = user.first_name + ' ' + user.last_name
    context = {
        'title': f'{name} | Spimebook',
        'target_user': user,
        'books': readed_books,
        'posts': posts,
    }
    return render(request, 'users/user.html', context)
