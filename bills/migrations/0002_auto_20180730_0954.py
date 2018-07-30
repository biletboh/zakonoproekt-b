# Generated by Django 2.0.7 on 2018-07-30 09:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('committees', '0003_auto_20180730_0926'),
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkOuts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Створено')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='Змінено')),
                ('slug', models.SlugField(max_length=512, unique=True, verbose_name='Посилання')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('date_passed', models.DateField(null=True, verbose_name='Дата')),
                ('date_got', models.DateField(null=True, verbose_name='Дата')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='document',
            old_name='phase_date',
            new_name='date',
        ),
        migrations.AddField(
            model_name='bill',
            name='agenda_last_date',
            field=models.DateField(null=True, verbose_name='Дата останньго розгляду'),
        ),
        migrations.AddField(
            model_name='bill',
            name='agenda_number',
            field=models.CharField(blank=True, max_length=100, verbose_name='Номер порядку денного'),
        ),
        migrations.AddField(
            model_name='bill',
            name='uri',
            field=models.URLField(blank=True, null=True, verbose_name='Посилання'),
        ),
        migrations.AlterField(
            model_name='agendaquestion',
            name='slug',
            field=models.SlugField(max_length=512, unique=True, verbose_name='Посилання'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='agenda_uri',
            field=models.URLField(blank=True, null=True, verbose_name='Посилання на порядок денний'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_type',
            field=models.CharField(max_length=100, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='committee_date_passed',
            field=models.DateField(blank=True, null=True, verbose_name='Дата направлення на комітети'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='registration_date',
            field=models.DateField(null=True, verbose_name='Дата реєстрації'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='rubric',
            field=models.CharField(max_length=100, verbose_name='Рубрика'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='session',
            field=models.CharField(max_length=100, verbose_name='Сесія'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='slug',
            field=models.SlugField(max_length=512, unique=True, verbose_name='Посилання'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='subject',
            field=models.CharField(max_length=100, verbose_name="Суб'єкт"),
        ),
        migrations.AlterField(
            model_name='bill',
            name='title',
            field=models.CharField(max_length=512, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='document',
            name='slug',
            field=models.SlugField(max_length=512, unique=True, verbose_name='Посилання'),
        ),
        migrations.AlterField(
            model_name='passing',
            name='slug',
            field=models.SlugField(max_length=512, unique=True, verbose_name='Посилання'),
        ),
        migrations.AddField(
            model_name='workouts',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bills.Bill'),
        ),
        migrations.AddField(
            model_name='workouts',
            name='committee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='committees.Committee'),
        ),
        migrations.AddField(
            model_name='bill',
            name='committees',
            field=models.ManyToManyField(related_name='bills', through='bills.WorkOuts', to='committees.Committee'),
        ),
    ]
