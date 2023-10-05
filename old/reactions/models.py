from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
# Create your models here.


class Love(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    post = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _("Love")
        verbose_name_plural = _("Loves")

    def __str__(self):
        return str(f'{self.user} love {self.post}')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    comment_date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    post = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return ("'{}'  by {} on {}".format(self.comment, self.user, self.post))
