# Generated by Django 5.1.5 on 2025-01-23 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_decoration_decoration_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='halls',
            name='photo_url',
            field=models.FileField(upload_to=''),
        ),
    ]
