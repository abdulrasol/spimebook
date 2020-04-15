# Generated by Django 3.0.4 on 2020-04-04 07:44

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_auto_20200403_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Novel', 'No'), ('Drama', 'Dr'), ('Fantasy', 'Fa'), ('Fiction', 'Fi'), ('Advanture', 'Ad')], max_length=37),
        ),
    ]
