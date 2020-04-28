from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from django.db.models.signals import post_save
from PIL import Image

# Create your models here.


class Author(models.Model):
    title = models.CharField(max_length=255)
    Author_Image = models.ImageField(
        upload_to='author/images', default='author.jpg')
    born_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.Author_Image.path)
        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.Author_Image.path)

    def __str__(self):
        if not self.en.name is None:
            return str(self.en.name)
        elif not self.ar.name is None:
            return str(self.en.name)
        else:
            return str(self.title)


class EN(models.Model):
    lang = models.CharField(max_length=2, default='en', auto_created='en')
    author = models.OneToOneField(
        Author, on_delete=models.CASCADE, verbose_name='Author')
    name = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name='Author Name')
    short = models.CharField(max_length=255, null=True,
                             blank=True, verbose_name='Short')
    author_Bio = models.TextField(
        null=True, blank=True, verbose_name='Author Bio')

    class Meta:
        verbose_name = _("English Translation)")
        verbose_name_plural = _("English Translation")

    def __str__(self):
        if self.name == None:
            return self.author.title
        else:
            return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class AR(models.Model):
    lang = models.CharField(max_length=2, default='ar', auto_created='ar')
    author = models.OneToOneField(
        Author, on_delete=models.CASCADE, verbose_name='Author')
    name = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name='Author Name')
    short = models.CharField(max_length=255, null=True,
                             blank=True, verbose_name='Short')
    author_Bio = models.TextField(
        null=True, blank=True, verbose_name='Author Bio')

    class Meta:
        verbose_name = ("Arabic Translateion)")
        verbose_name_plural = ("Arabic Translateion")

    def __str__(self):
        if self.name == None:
            return self.author.title
        else:
            return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class FR(models.Model):
    lang = models.CharField(max_length=2, default='fr', auto_created='fr')
    author = models.OneToOneField(
        Author, on_delete=models.CASCADE, verbose_name='Author')
    name = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name='Author Name')
    short = models.CharField(max_length=255, null=True,
                             blank=True, verbose_name='Short')
    author_Bio = models.TextField(
        null=True, blank=True, verbose_name='Author Bio')

    class Meta:
        verbose_name = ("French Translateion)")
        verbose_name_plural = ("French Translateion")

    def __str__(self):
        if self.name == None:
            return self.author.title
        else:
            return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


def create_langs(sender, **kwargs):
    if kwargs['created']:
        EN.objects.create(author=kwargs['instance'])
        AR.objects.create(author=kwargs['instance'])
        FR.objects.create(author=kwargs['instance'])


post_save.connect(create_langs, sender=Author)
