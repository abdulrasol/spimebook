from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from posts.models import Post
from books.models import Book
from django.conf import settings
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    picture = models.ImageField(
        upload_to='users/Profiles/', blank=True, null=True, default='user.png')
    bio = models.CharField(max_length=221, blank=True, null=True)
    loves = models.ManyToManyField(
        Post, related_name='loves', blank=True)
    books = models.ManyToManyField(
        Book, related_name='books', blank=True)
    lang = models.CharField(
        max_length=2, choices=settings.LANGUAGES, default='en')

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)

        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.picture.path)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
