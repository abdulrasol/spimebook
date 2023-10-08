from django.urls import path
from .views import BooksList, GenresList, BookDetail,GenresDetail
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'books'
urlpatterns = [
    path('', BooksList.as_view(), name='books-list'),
    path('<int:pk>/', BookDetail.as_view(), name='book'),
    path('genres/', GenresList.as_view(), name='genres-list'),
    path('genres/<int:pk>/', GenresDetail.as_view(), name='genre'),

]
urlpatterns = format_suffix_patterns(urlpatterns)

