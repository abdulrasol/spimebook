from django import forms
from django.forms import ModelForm
from .models import Comment, Post


class AddCommentForm(forms.Form):
    comment = forms.CharField(max_length=255)


class EditPostForm(ModelForm):
    archived = forms.BooleanField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'for_book', 'post_type', 'archived']
