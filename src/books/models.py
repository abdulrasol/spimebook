from django.db import models
from django.utils import timezone
#from multiselectfield import MultiSelectField
from PIL import Image


# Create your models here.

# Book Author


class Author(models.Model):
    author_Name = models.CharField(max_length=255)
    Author_Image = models.ImageField(
        upload_to='books/author/', default='author.jpg')
    born_date = models.DateField(default=timezone.now)
    short = models.CharField(max_length=255, null=True, default='')
    author_Bio = models.TextField(max_length=5000, null=True, default='')

    def __str__(self):
        return self.author_Name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.Author_Image.path)
        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.Author_Image.path)


class Genres(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre


class Book(models.Model):
    book_type = [
        ('Book', 'Book'),
        ('Novel', 'Novel')
    ]

    title = models.CharField(max_length=255)
    book_image = models.ImageField(
        upload_to='books/cover/', default='book.jpg')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publish_date = models.DateField(default=timezone.now)
    genres = models.ManyToManyField(Genres, related_name='genres')
    book_Bio = models.TextField(default='')
    book_or_Novel = models.CharField(
        max_length=5, choices=book_type, default='Book')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.book_image.path)
        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.book_image.path)
