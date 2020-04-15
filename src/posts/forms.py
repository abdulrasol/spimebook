from django import forms
from django.forms import ModelForm
from .models import Comment


class AddCommentForm(forms.Form):
    comment = forms.CharField(max_length=255)
