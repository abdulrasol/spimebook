# Generated by Django 3.0.4 on 2020-04-09 08:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0011_auto_20200409_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]
