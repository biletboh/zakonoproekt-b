# Generated by Django 2.0.7 on 2018-09-07 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0006_auto_20180907_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='agenda_last_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата останньго розгляду'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='agenda_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер порядку денного'),
        ),
    ]
