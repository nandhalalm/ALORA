# Generated by Django 5.1.5 on 2025-01-24 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_food_food_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='decoration',
            name='decoration_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
