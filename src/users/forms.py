from django import forms
from .models import Profile


class EditProfileForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput)
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ['bio', 'picture']
