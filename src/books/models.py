from django.db import models, DatabaseError
from django.utils import timezone
from PIL import Image
from django.shortcuts import reverse
from django.db.models.signals import post_save
from authors.models import Author
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf import settings
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.

book_type = [
    ('Book', _('Book')),
    ('Novel', _('Novel'))
]


class Genres(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Book Title'))
    book_image = models.ImageField(
        upload_to='books/cover/', default='book.jpg', verbose_name=_('Book Cover Image'))
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, verbose_name=_('The Author'))
    publish_date = models.DateField(
        default=timezone.now, verbose_name=_('Publish Date'))
    genres = models.ManyToManyField(
        Genres, related_name='genres', verbose_name=_('Genres'), blank=True)
    book_or_Novel = models.CharField(
        max_length=5, choices=book_type, default='Book', verbose_name=_('Type'))
    ratings = GenericRelation(Rating, related_query_name='foos')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.book_image.path)
        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.book_image.path)


class Rating(models.Model):
    class Meta:
        unique_together = (('book', 'user'),)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f'{self.user} rate {self.book} by {self.rating} from 5'


class BookManager(models.Manager):
    pass
