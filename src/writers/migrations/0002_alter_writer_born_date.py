# Generated by Django 4.2.6 on 2023-10-08 12:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writer',
            name='born_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Writwe Birth Date'),
        ),
    ]