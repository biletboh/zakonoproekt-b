# Generated by Django 2.0.7 on 2018-09-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiators', '0007_auto_20180910_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initiator',
            name='convocation',
            field=models.CharField(max_length=25, verbose_name='Скликання'),
        ),
    ]
