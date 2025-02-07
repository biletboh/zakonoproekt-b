# Generated by Django 2.0.7 on 2018-07-29 12:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Створено')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='Змінено')),
                ('slug', models.SlugField(unique=True, verbose_name='Посилання')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('head', models.CharField(blank=True, max_length=200, verbose_name='Заголовок')),
                ('description', models.CharField(blank=True, max_length=512, verbose_name='Заголовок')),
                ('number', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Кількісний склад')),
                ('website', models.CharField(blank=True, max_length=100, verbose_name='Вебсайт')),
                ('secretary', models.CharField(blank=True, max_length=100, verbose_name='Сектретар')),
                ('secretary_contacts', models.CharField(blank=True, max_length=100, verbose_name='Контакти секретаря')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkOuts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Створено')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='Змінено')),
                ('slug', models.SlugField(unique=True, verbose_name='Посилання')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('date_passed', models.DateField(null=True, verbose_name='Дата')),
                ('date_got', models.DateField(null=True, verbose_name='Дата')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='committee_workouts', to='bills.Bill')),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to='committees.Committee')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]
