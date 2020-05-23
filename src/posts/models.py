from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext as _
from books.models import Book

# Create your models here.


class Post(models.Model):
    POST_TYPE = [
        ('Q', _('Quote')),
        ('R', _('Review')),
        ('P', _('Post')),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('User'))
    lang = models.CharField(max_length=2, default='en',
                            verbose_name=_('Language'))
    title = models.CharField(
        max_length=120, default='', verbose_name=_('Title'))
    post_date = models.DateTimeField(
        default=timezone.now, verbose_name=_('Publish Date'))
    content = models.TextField(default='', verbose_name=_('Content'))
    for_book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('For Book'))
    archived = models.BooleanField(default=False)
    post_type = models.CharField(
        max_length=1,
        choices=POST_TYPE,
        default='Psot', verbose_name=_('Post Type'))
    loves = GenericRelation('reactions.Love')
    comments = GenericRelation('reactions.Comment')

    def __str__(self):
        return '{} for {}'.format(self.title, self.for_book)

    class Meta:
        ordering = ["-post_date"]
