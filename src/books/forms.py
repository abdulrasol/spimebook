from django import forms
from .models import Author, Book


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_image', 'genres']
