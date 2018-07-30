from django.db import models

from transliterate import slugify
from model_utils import Choices

from core.models import BaseModel
from committees.models import Committee
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
        self.slug = slugify(f'{self.title} {self.id}')
        super().save(*args, **kwargs)


class Bill(BaseModel):
    """Store information about a bill."""

    CONVOCATION = Choices((8, 'VIII', 'VIII скликання'))

    title = models.CharField('Заголовок', max_length=512)
    rada_id = models.PositiveIntegerField('ID у ВР')
    uri = models.URLField('Посилання', null=True,
                          blank=True)
    number = models.PositiveIntegerField('Реєстраційний номер')
    convocation = models.PositiveSmallIntegerField(
        choices=CONVOCATION, default=CONVOCATION.VIII)
    session = models.CharField('Сесія', max_length=100)
    rubric = models.CharField('Рубрика', max_length=100)
    subject = models.CharField("Суб'єкт", max_length=100)
    bill_type = models.CharField('Тип', max_length=100)
    phase = models.CharField('Фаза', max_length=200)
    phase_date = models.DateField('Дата фази')
    registration_date = models.DateField('Дата реєстрації', null=True)
    agenda_number = models.CharField('Номер порядку денного', max_length=100,
                                     blank=True)
    agenda_last_date = models.DateField('Дата останньго розгляду', null=True)
    agenda_uri = models.URLField('Посилання на порядок денний', null=True,
                                 blank=True)
    committee_date_passed = models.DateField('Дата направлення на комітети',
                                             null=True, blank=True)

    bind_bills = models.ManyToManyField('self', symmetrical=True)
    alternatives = models.ManyToManyField('self', symmetrical=True)

    authors = models.ManyToManyField(Initiator, related_name='authored')
    executives = models.ManyToManyField(Initiator,
                                        related_name='bills_to_execute')
    main_executives = models.ManyToManyField(
        Initiator, related_name='main_bills_to_execute')

    chronology = models.ManyToManyField(Passing, related_name='bills')

    committees = models.ManyToManyField(Committee, through='WorkOuts',
                                        related_name='bills')

    class Meta:
        verbose_name_plural = 'bills'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


def bill_directory_path(instance, filename):
    return f'{instance.bill.title}'


class Document(BaseModel):
    """Store data about documents related to bills."""

    document_type = models.CharField('Тип', max_length=50)
    date = models.DateField('Дата')
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


class WorkOuts(BaseModel):
    """Store data about documents related to bills."""

    title = models.CharField('Заголовок', max_length=200)
    date_passed = models.DateField('Дата', null=True)
    date_got = models.DateField('Дата', null=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.bill.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
