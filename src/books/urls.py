from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.books, name='books'),
    path('books/add/', views.add_book, name='add-book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit-book'),
    path('books/<int:book_id>/', views.book, name='book'),
    path('books/<str:genre>/', views.genres, name='fliter-genre'),
    path('authors/add/', views.add_author, name='add-author'),
    path('authors/<int:author_id>/<str:book_author>/',
         views.author, name='author'),
    path('authors/<int:author_id>/<str:author_name>/edit/',
         views.edit_author, name='edit-author'),
    # ajax
    path('ajax/book/readed/<int:book_id>',
         views.readed_book, name='readed-book'),
    path('ajax/book/search',
         views.search_book, name='search-book'),
    path('ajax/book/search/<str:book_title_author>',
         views.book_by_ajax, name='ajax-book'),
    path('ajax/author/author_autocomplete/',
         views.author_autocomplete, name='author-autocomplete'),


]
