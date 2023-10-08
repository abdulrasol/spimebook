from PIL import Image
from django.db import models
from writers.models import Writer

book_type = [
    ('b', 'Book'),
    ('n', 'Novel'),
]


# Create your models here.
class Genres(models.Model):
    genre = models.CharField(max_length=256, verbose_name="Genre")

    def __str__(self):
        return self.genre


class Book(models.Model):
    title = models.CharField(max_length=256, verbose_name="Book Title")
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, verbose_name="Book Writer")
    image = models.ImageField(upload_to='books/cover/', default='book.jpg', verbose_name='Book Cover')
    genres = models.ManyToManyField(Genres, verbose_name='Book Genres')
    pub_date = models.DateField(null=True, verbose_name='Publish Date')
    type = models.CharField(choices=book_type, verbose_name='Book or Novel', max_length=5)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        img = Image.open(self.image.path)
        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.book_image.path)
        super().save(*args, **kwargs)
