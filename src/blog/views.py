from django.shortcuts import render
from .models import blogs
# Create your views here.


def blog(request):
    bloges = blogs.objects.all()
    context = {
        'title': 'Spimebook Blog',
        'blogs': bloges
    }
    return render(request, 'blog/index.html', context)
