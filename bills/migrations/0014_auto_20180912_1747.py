# Generated by Django 2.0.7 on 2018-09-12 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0013_auto_20180912_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='uri',
            field=models.URLField(blank=True, default='', verbose_name='Посилання'),
            preserve_default=False,
        ),
    ]
