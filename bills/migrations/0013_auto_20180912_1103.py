# Generated by Django 2.0.7 on 2018-09-12 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0012_remove_bill_committee_date_passed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='date',
            field=models.DateField(null=True, verbose_name='Дата'),
        ),
    ]
