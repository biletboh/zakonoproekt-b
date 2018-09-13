# Generated by Django 2.0.7 on 2018-09-13 16:29

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('initiators', '0009_auto_20180911_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Створено')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='Змінено')),
                ('number', models.PositiveSmallIntegerField(blank=True, choices=[(8, 'VIII скликання')], null=True, unique=True, verbose_name='Конвокація')),
                ('latin_number', models.CharField(blank=True, max_length=25, verbose_name='Конвокація (лат.)')),
                ('slug', models.SlugField(max_length=90, null=True, unique=True, verbose_name='Посилання')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='initiator',
            name='convocation',
        ),
        migrations.AddField(
            model_name='initiator',
            name='convocation',
            field=models.ManyToManyField(blank=True, related_name='initiators', to='initiators.Convocation'),
        ),
    ]
