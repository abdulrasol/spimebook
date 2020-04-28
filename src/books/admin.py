from django.contrib import admin
from .models import Book, Author, Genres, Rating, AR, EN, FR

# Register your models here.
admin.site.register(Book)
admin.site.register(AR)
admin.site.register(EN)
admin.site.register(FR)
admin.site.register(Genres)
# admin.site.register(Rating)
