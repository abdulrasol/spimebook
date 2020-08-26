from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from posts.models import Post
from .models import Profile
from django.http import HttpResponse
from .forms import EditProfileForm, EditAccountForm
from django.utils.translation import gettext as _, activate, LANGUAGE_SESSION_KEY, get_language_from_request
from django.conf import settings as conf_settings
from django.http import JsonResponse
from django_ajax.decorators import ajax
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
# { % if user.is_authenticated % }


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            activate(user.profile.lang)
            response = redirect('/')
            response.set_cookie(
                conf_settings.LANGUAGE_COOKIE_NAME, user.profile.lang)
            return response
        else:
            messages.add_message(request, messages.WARNING,
                                 f'{username} or password error')
            redirect('log-in')
    response = render(request, 'users/login.html', {})
    return response


@login_required(login_url='log-in')
def log_out(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':  # check
        if User.objects.filter(username=request.POST['username']).exists() or User.objects.filter(email=request.POST['email']).exists():
            messages.add_message(request, messages.SUCCESS,
                                 'username or email are taken')
            return redirect('register')

        else:
            language = request.POST['language']
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            # print(username, password, email)
            user = User.objects.create_user(username, email, password)
            user.save()
            user.profile.lang = language
            user.profile.save()
            messages.add_message(request, messages.SUCCESS,
                                 f'Welcome {username}, your account created login now!')
            response = redirect('log-in')
            activate(user.profile.lang)
            response.set_cookie(
                conf_settings.LANGUAGE_COOKIE_NAME, user.profile.lang)
            return response

    return render(request, 'users/register.html', {'user_exists': False})


@login_required(login_url='log-in')
def profile(request):
    user = request.user
    # print(request.user)
    all_posts = Post.objects.filter(user=user)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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
def settings(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        language = request.POST['language']
        user = request.user
        if username != '':
            if not User.objects.filter(username=username).exists():
                user.username = username
            else:
                messages.add_message(request, messages.SUCCESS,
                                     f'{username} is taken')
                return redirect('settings')
        if email != '':
            if not User.objects.filter(email=email).exists():
                # print(email)
                user.email = email
            else:
                messages.add_message(request, messages.SUCCESS,
                                     f'{email} is taken')
                return redirect('settings')
        if password != '':
            if len(password) >= 6:
                user.set_password(password)
            else:
                messages.add_message(
                    request, messages.SUCCESS, 'Password you entered less than 6 char!')
                return redirect('settings')
        user.profile.lang = language
        user.profile.save()
        user.save()
        return redirect('profile')

    context = {
        'title': 'Account Settings',
    }
    return render(request, 'users/settings.html', context)


@login_required(login_url='log-in')
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    form = EditProfileForm(request.POST or None,
                           request.FILES or None, instance=profile)
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        # print(request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            profile.user.first_name = firstname
            profile.user.last_name = lastname
            profile.user.save()
            return redirect('/user/profile')
        else:
            form = EditProfileForm(initial=request.POST)
    context = {
        'title': 'Edit my profile',
        'form': form
    }
    return render(request, 'users/edit_porfile.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    # print(f'userfrom url {username} and from db {user}')
    all_posts = Post.objects.filter(user=user).filter(archived=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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


def revover_password(request):
    title = _('Recover your password')
    context = {
        'title': title
    }
    response = render(request, 'users/recover_password.html', context)
    return response


@ajax
def send_token_pass(request):
    email = request.POST['email']
    if User.objects.filter(email=email).exists():
        user = get_object_or_404(User, email=email)
        import random
        token = random.randrange(10000, 99999)
        user.profile.pass_recover_token = token
        user.profile.save()
        mailing({'name': user.get_full_name(), 'token': token}, user.email)
        return {'state': True}
    else:
        return {'state': False}


@ajax
def check_token_pass(request):
    email = request.POST['email'].lower()
    token = request.POST['token']
    user = get_object_or_404(User, email=email)
    if token == user.profile.pass_recover_token:
        return {'state': True}
    else:
        return {'state': False}


@ajax
def set_new_pass(request):
    email = request.POST['email'].lower()
    token = request.POST['token']
    password = request.POST['password']
    default = request.POST['csrfmiddlewaretoken']
    user = get_object_or_404(User, email=email)
    if token == user.profile.pass_recover_token:
        user.set_password(password)
        user.save()
        user.profile.pass_recover_token = default
        user.profile.save()
        return {'state': True}
    else:
        return {'state': False, 'msg': 'Error Token'}


def mailing(data={}, *recipient_list):
    recipient_list = list(recipient_list)
    html_message = render_to_string(
        'users/email/token_code.html', context=data)
    plan_text = strip_tags(html_message)
    send_mail('Subject', plan_text, 'spimebook@gmail.com',
              recipient_list, fail_silently=False, html_message=html_message)
