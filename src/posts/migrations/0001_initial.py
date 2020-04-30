# Generated by Django 3.0.5 on 2020-04-30 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_edit_date', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(default='')),
                ('post_type', models.CharField(choices=[('Q', 'Quote'), ('R', 'Reviw'), ('P', 'Post')], default='Psot', max_length=1)),
                ('for_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-post_date'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=120)),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_edit_date', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(default='')),
                ('post_type', models.CharField(choices=[('Q', 'Quote'), ('R', 'Reviw'), ('P', 'Post')], default='Psot', max_length=1)),
                ('archived', models.BooleanField(default=False)),
                ('for_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-post_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
