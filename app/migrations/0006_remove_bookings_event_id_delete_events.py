# Generated by Django 5.1.5 on 2025-01-24 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_decoration_decoration_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='event_id',
        ),
        migrations.DeleteModel(
            name='Events',
        ),
    ]
