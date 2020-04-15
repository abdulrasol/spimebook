from django.contrib import admin
from .models import Book, Author, Genres

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Genres)
