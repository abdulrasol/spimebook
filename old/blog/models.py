from django.db import models
from django.contrib.auth.admin import User
from django.utils import timezone

# Create your models here.


class blogs(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class meta:
        ordering = ('-date')
