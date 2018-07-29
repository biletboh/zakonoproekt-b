from django.db import models

from transliterate import slugify
from model_utils import Choices

from core.models import BaseModel
from initiators.models import Initiator


class Passing(BaseModel):
    """Store information about a bill."""

    title = models.CharField('Заголовок', max_length=200)
    date = models.DateField('Дата')

    class Meta:
        verbose_name_plural = 'passings'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Bill(BaseModel):
    """Store information about a bill."""

    CONVOCATION = Choices((8, 'VIII', 'VIII скликання'))

    title = models.CharField('Заголовок', max_length=200)
    rada_id = models.PositiveIntegerField('ID у ВР')
    number = models.PositiveIntegerField('Реєстраційний номер')
    convocation = models.PositiveSmallIntegerField(
        choices=CONVOCATION, default=CONVOCATION.VIII)
    session = models.CharField('Сесія', max_length=30)
    rubric = models.CharField('Рубрика', max_length=50)
    subject = models.CharField("Суб'єкт", max_length=50)
    bill_type = models.CharField('Тип', max_length=50)
    phase = models.CharField('Фаза', max_length=200)
    phase_date = models.DateField('Дата фази')
    registration_date = models.DateTimeField('Дата реєстрації', null=True)
    agenda_uri = models.URLField('Посилання на порядок дений', null=True,
                                 blank=True)
    committee_date_passed = models.DateField('Дата фази', null=True,
                                             blank=True)

    bind_bills = models.ManyToManyField('self', symmetrical=True)
    alternatives = models.ManyToManyField('self', symmetrical=True)

    authors = models.ManyToManyField(Initiator, related_name='authored')
    executives = models.ManyToManyField(Initiator,
                                        related_name='bills_to_execute')
    main_executives = models.ManyToManyField(
        Initiator, related_name='main_bills_to_execute')

    chronology = models.ManyToManyField(Passing, related_name='bills')

    class Meta:
        verbose_name_plural = 'bills'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


def bill_directory_path(instance, filename):
    return f'{instance.title}'


class Document(BaseModel):
    """Store data about documents related to bills."""

    document_type = models.CharField('Тип', max_length=50)
    phase_date = models.DateField('Дата')
    uri = models.URLField('Посилання на порядок дений', null=True, blank=True)
    document_file = models.FileField(upload_to=bill_directory_path)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE,
                             related_name='documents')

    def __str__(self):
        return f'{self.document_type} {self.bill.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.document_type} {self.bill.title}')
        super().save(*args, **kwargs)


class AgendaQuestion(BaseModel):
    """Store data about Rada agenda."""

    TYPE = Choices((1, 'registration', 'Реєстрація'),
                   (0, 'vote', 'Голосування'),
                   (8, 'speech', 'Промова')
                   )

    bills = models.ManyToManyField(Bill, related_name='agenda_questions')
    title = models.CharField('Заголовок', max_length=512)
    question_type = models.PositiveSmallIntegerField(choices=TYPE)
    id_event = models.PositiveIntegerField('ID події')
    vote_for = models.PositiveSmallIntegerField('За')
    vote_against = models.PositiveSmallIntegerField('Проти')
    vote_abstain = models.PositiveSmallIntegerField('Утрималися')
    not_voting = models.PositiveSmallIntegerField('Не голосували')
    present = models.PositiveSmallIntegerField('Присутні')
    absent = models.PositiveSmallIntegerField('Відсутні')
    total = models.PositiveSmallIntegerField('Загалом')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
