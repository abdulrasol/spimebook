from rest_framework import generics, permissions

from .serializers import BookSerializer, GenresSerializer
from .models import Genres, Book


# Create your views here.

class BooksList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class GenresList(generics.ListAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class GenresDetail(generics.RetrieveAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

