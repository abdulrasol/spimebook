from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from django.db.models.signals import post_save
from PIL import Image
from django.conf import settings

# Create your models here.

BASE = _('Author')
NAME = _('Author Name')
SHORT = _('Short')
BIO = _('Author Bio')


class Author(models.Model):
    title = models.CharField(max_length=255)
    Author_Image = models.ImageField(
        upload_to='author/images', default='author.jpg', verbose_name=_('Author Profile Image'))
    born_date = models.DateField(
        default=timezone.now, verbose_name=_('Birth Date'))

    def __str__(self):
        if self.title is None:
            return str(self.en.name)
        else:
            return self.title

    def translate(self, lang):
        if lang in settings.LANGUAGES:
            print('IS')
        lang = lang.lower()
        translated = eval(f"self.{lang}")
        return translated

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.Author_Image.path)
        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.Author_Image.path)
