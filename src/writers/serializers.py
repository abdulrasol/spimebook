from rest_framework import serializers
from .models import Writer
from books.serializers import BookSerializer


class WriterSerializer(serializers.HyperlinkedModelSerializer):

    # SerializerMethodField to represent related books
    books = serializers.SerializerMethodField()
    '''
    books = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='books:book'  # Replace with the actual view name for the Book detail view
    )
    '''
    class Meta:
        model = Writer
        fields = ['id', 'name', 'bio', 'image', 'short', 'born_date', 'books']

        # Custom method to get and serialize related books

    def get_books(self, obj):
        # Assuming you have a related_name on the ForeignKey in Book model
        books = obj.book_set.all()
        # Serialize the related books using BookSerializer
        serializer = BookSerializer(books, many=True, context=self.context)
        return serializer.data