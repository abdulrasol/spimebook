from django.contrib import admin
from .models import Book, Author, Genres, Rating

# Register your models here.
admin.site.register(Book)
admin.site.register(Genres)
