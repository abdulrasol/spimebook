# Generated by Django 4.2.6 on 2023-10-08 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('picture', models.ImageField(blank=True, default='user.png', null=True, upload_to='users/Profiles/', verbose_name='Profile Picture')),
                ('bio', models.CharField(blank=True, max_length=221, null=True, verbose_name='Bio')),
            ],
        ),
    ]