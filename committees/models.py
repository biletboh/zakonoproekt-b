from django.db import models

from transliterate import slugify

from core.models import BaseModel


class Committee(BaseModel):
    """Store data about committees."""

    title = models.CharField('Заголовок', max_length=200)
    head = models.CharField('Голова', max_length=200, blank=True)
    description = models.CharField('Опис', max_length=512, blank=True)
    number = models.PositiveSmallIntegerField('Кількісний склад',
                                              null=True, blank=True)
    website = models.CharField('Вебсайт', max_length=100, blank=True)
    secretary = models.CharField('Сектретар', max_length=100, blank=True)
    secretary_contacts = models.CharField('Контакти секретаря',
                                          max_length=100, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
