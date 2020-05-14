from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from books.models import Book

# Create your models here.


class Post(models.Model):
    POST_TYPE = [
        ('Q', 'Quote'),
        ('R', 'Reviw'),
        ('P', 'Post'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang = models.CharField(max_length=2, default='en')
    title = models.CharField(max_length=120, default='')
    post_date = models.DateTimeField(default=timezone.now)
    content = models.TextField(default='')
    for_book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, blank=True, null=True)
    archived = models.BooleanField(default=False)
    post_type = models.CharField(
        max_length=1,
        choices=POST_TYPE,
        default='Psot')
    loves = GenericRelation('reactions.Love')
    comments = GenericRelation('reactions.Comment')

    def __str__(self):
        return '{} for {}'.format(self.title, self.for_book)

    class Meta:
        ordering = ["-post_date"]
