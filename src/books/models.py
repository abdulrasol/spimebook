from django.db import models
from django.utils import timezone
from PIL import Image
from django.shortcuts import reverse
from django.db.models.signals import post_save
from authors.models import Author
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from googletrans import Translator
from django.conf import settings
# Create your models here.

translator = Translator()
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
        Genres, related_name='genres', verbose_name=_('Genres'))
    book_or_Novel = models.CharField(
        max_length=5, choices=book_type, default='Book', verbose_name=_('Type'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.book_image.path)
        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.book_image.path)


class AR(models.Model):
    lang = models.CharField(max_length=2, default='ar', auto_created='ar')
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, verbose_name=_('Orginal Book'))
    title = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name=_('Book Title'))
    book_Bio = models.TextField(
        blank=True, null=True, verbose_name=_('Book Bio'))

    class Meta:
        verbose_name = _("Arabic Translation")
        verbose_name_plural = _("Arabic Translation")
        ordering = ['-id']

    def __str__(self):
        if self.title is None:
            return translator.translate(self.book.title, dest='ar').text
        else:
            return self.title

    def get_absolute_url(self):
        return reverse("AR_detail", kwargs={"pk": self.pk})


class EN(models.Model):
    lang = models.CharField(max_length=2, default='en', auto_created='en')
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, verbose_name=_('Orginal Book'))
    title = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name=_('Book Title'))
    book_Bio = models.TextField(
        blank=True, null=True, verbose_name=_('Book Bio'))

    class Meta:
        verbose_name = _("English Translation")
        verbose_name_plural = _("English Translation")
        ordering = ['-id']

    def __str__(self):
        if self.title is None:
            return translator.translate(self.book.title, dest='en').text
        else:
            return self.title

    def get_absolute_url(self):
        return reverse("EN_detail", kwargs={"pk": self.pk})


class FR(models.Model):
    lang = models.CharField(max_length=2, default='fr', auto_created='fr')
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, verbose_name=_('Orginal Book'))
    title = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name=_('Book Title'))
    book_Bio = models.TextField(
        blank=True, null=True, verbose_name=_('Book Bio'))

    class Meta:
        verbose_name = _("French Translation")
        verbose_name_plural = _("French Translation")
        ordering = ['-id']

    def __str__(self):
        if self.title is None:
            return translator.translate(self.book.title, dest='fr').text
        else:
            return self.title

    def get_absolute_url(self):
        return reverse("FR_detail", kwargs={"pk": self.pk})

##


def create_langs(sender, **kwargs):
    if kwargs['created']:
        for lang in settings.SUPPORTED_LANGS:
            eval(f"{lang}.objects.create(book=kwargs['instance'])")


post_save.connect(create_langs, sender=Book)
##


class Rating(models.Model):
    class Meta:
        unique_together = (('book', 'user'),)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f'{self.user} rate {self.book} by {self.rating} from 10'
