from django.db import models
import datetime
from PIL import Image

# Create your models here.


class Writer(models.Model):
    name = models.CharField(verbose_name='Writer name', max_length=256)
    short = models.CharField(
        verbose_name='Short text about writer', max_length=255, null=True, blank=True)
    bio = models.TextField(
        verbose_name='Writer Full Bio', null=True, blank=True)
    image = models.ImageField(verbose_name='Writer Profile Image',
                              upload_to='author/images', default='author.jpg')
    born_date = models.DateField(
        verbose_name='Writwe Birth Date', default=datetime.date.today)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.image.path)
