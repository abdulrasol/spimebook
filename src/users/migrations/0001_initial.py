# Generated by Django 3.0.5 on 2020-04-30 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('picture', models.ImageField(blank=True, default='user.png', null=True, upload_to='users/Profiles/')),
                ('bio', models.CharField(blank=True, max_length=221, null=True)),
                ('lang', models.CharField(choices=[('en', 'English'), ('ar', 'العربية'), ('fr', 'français'), ('ru', 'русский'), ('es', 'Spanish'), ('de', 'Deutsch'), ('it', 'Italiano')], default='en', max_length=2, verbose_name='Language')),
                ('books', models.ManyToManyField(blank=True, related_name='books', to='books.Book')),
                ('loves', models.ManyToManyField(blank=True, related_name='loves', to='posts.Post')),
            ],
        ),
    ]
