from django import forms
from django.forms import ModelForm
from .models import Post


class EditPostForm(ModelForm):
    archived = forms.BooleanField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'for_book', 'archived']
