# Generated by Django 2.0.7 on 2018-09-11 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0009_auto_20180910_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workouts',
            name='slug',
            field=models.SlugField(max_length=512, null=True, unique=True, verbose_name='Посилання'),
        ),
    ]
