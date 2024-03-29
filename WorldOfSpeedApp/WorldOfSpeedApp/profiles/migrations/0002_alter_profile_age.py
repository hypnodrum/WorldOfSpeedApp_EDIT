# Generated by Django 4.2.10 on 2024-03-05 07:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(blank=True, help_text='Age requirement: 21 years and above.', null=True, validators=[django.core.validators.MinValueValidator(21)]),
        ),
    ]
