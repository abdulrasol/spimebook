from rest_framework import serializers
from .models import Book, Genres
from writers.models import Writer


class GenresSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Genres
        fields = ['id', 'genre', 'books']

    def get_books(self, obj):
        books = obj.book_set.all()
        serializer = BookSerializer(books, many=True, context=self.context)
        return serializer.data


class BookSerializer(serializers.HyperlinkedModelSerializer):
    writer = serializers.HyperlinkedRelatedField(view_name='writers:writer', read_only=True)
    genres = serializers.HyperlinkedRelatedField(view_name='books:genre', many=True,
                                                 read_only=True)  # GenresSerializer(many=True) #serializers.HyperlinkedIdentityField(view_name='books:genres-list', many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'writer', 'image', 'pub_date', 'type', 'genres']
