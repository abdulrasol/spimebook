from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile', verbose_name='User')
    image = models.ImageField(
        upload_to='users/Profiles/', blank=True, null=True, default='user.png', verbose_name='Profile Picture')
    bio = models.CharField(max_length=221, blank=True,
                           null=True, verbose_name='Bio')
    # posts = models.ManyToManyRel('Posts.Post')

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 250 or img.height > 250:
            size = (250, 250)
            img.thumbnail(size)
            img.save(self.picture.path)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
