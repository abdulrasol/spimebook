
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from books.models import Book

# Create your models here.


class UserPost(models.Model):
    POST_TYPE = [
        ('Q', 'Quote'),
        ('R', 'Reviw'),
        ('P', 'Post'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)
    post_edit_date = models.DateTimeField(auto_now=timezone.now)
    content = models.TextField(default='')
    post_type = models.CharField(
        max_length=1,
        choices=POST_TYPE,
        default='Psot')
    for_book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return '{} post on {}'.format(self.user, self.for_book)

    class Meta:
        ordering = ["-post_date"]


class Post(models.Model):
    POST_TYPE = [
        ('Q', 'Quote'),
        ('R', 'Reviw'),
        ('P', 'Post'),
    ]
    title = models.CharField(max_length=120, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)
    post_edit_date = models.DateTimeField(auto_now=timezone.now)
    content = models.TextField(default='')
    post_type = models.CharField(
        max_length=1,
        choices=POST_TYPE,
        default='Psot')
    for_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return '{} for {}'.format(self.title, self.for_book)

    class Meta:
        ordering = ["-post_date"]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    comment_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return ("'{}'  by {} on {}".format(self.comment, self.user, self.post))
