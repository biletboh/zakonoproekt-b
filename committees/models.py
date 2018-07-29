from django.db import models

from transliterate import slugify

from bills.models import Bill
from core.models import BaseModel


class Committee(BaseModel):
    """Store data about committees."""

    title = models.CharField('Заголовок', max_length=200)
    head = models.CharField('Заголовок', max_length=200, blank=True)
    description = models.CharField('Заголовок', max_length=512, blank=True)
    number = models.PositiveSmallIntegerField('Кількісний склад',
                                              null=True, blank=True)
    website = models.CharField('Вебсайт', max_length=100, blank=True)
    secretary = models.CharField('Сектретар', max_length=100, blank=True)
    secretary_contacts = models.CharField('Контакти секретаря',
                                          max_length=100, blank=True)

    def __str__(self):
        return f'{self.title} {self.bill.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class WorkOuts(BaseModel):
    """Store data about documents related to bills."""

    title = models.CharField('Заголовок', max_length=200)
    date_passed = models.DateField('Дата', null=True)
    date_got = models.DateField('Дата', null=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE,
                             related_name='committee_workouts')
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE,
                                  related_name='workouts')

    def __str__(self):
        return f'{self.title} {self.bill.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
