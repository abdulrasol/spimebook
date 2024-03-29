from django.urls import path
from . import views
app_name = 'books'
urlpatterns = [
    path('', views.books, name='books'),
    path('add/', views.add_book, name='add-book'),
    path('<int:book_id>/edit/', views.edit_book, name='edit-book'),
    path('<int:book_id>/', views.book, name='book'),
    path('<int:book_id>/<str:posts>', views.book, name='filter-book-post'),
    path('filter/<str:genre>/', views.genres, name='fliter-genre'),
    path('type/<str:book_type>/', views.book_or_novel, name='fliter-type'),

    # ajax
    path('ajax/book/readed/<int:book_id>',
         views.readed_book, name='readed-book'),
    path('ajax/book/search',
         views.search_book, name='search-book'),
    path('ajax/book/search/<str:book_title_author>',
         views.book_by_ajax, name='ajax-book'),
    path('ajax/book/rate/<int:book_id>/<int:rating>',
         views.rating_book, name='rate-book'),
    path('ajax/genre/<str:genre>',
         views.add_genre, name='add-genre'),
]
