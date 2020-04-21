from django import forms
from .models import Profile
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput, required=False)
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ['bio', 'picture']


class EditAccountForm(forms.ModelForm):
    password = forms.PasswordInput(render_value='')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
