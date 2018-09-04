import random
from django.db import models
from core.models import BaseModel

from model_utils import Choices
from easy_thumbnails.fields import ThumbnailerImageField
from transliterate import slugify


def photo_upload_to(instance, filename):
    return (f'initiators/{instance.first_name}_{instance.last_name}'
            + f'/{instance.id}')


class Initiator(BaseModel):
    """Store information about initiators of bills."""

    CONVOCATION = Choices((8, 'VIII', 'VIII скликання'))

    first_name = models.CharField("Ім'я", max_length=50)
    last_name = models.CharField('Прізвище', max_length=100)
    middle_name = models.CharField('По батькові', max_length=100,
                                   blank=True)
    convocation = models.PositiveSmallIntegerField(
        choices=CONVOCATION, default=CONVOCATION.VIII)
    rada_id = models.PositiveSmallIntegerField(unique=True)
    party = models.CharField('Партія', max_length=200, blank=True)
    faction = models.CharField('Фракція', max_length=200, blank=True)
    information = models.CharField('Інформація', max_length=512, blank=True)
    email = models.EmailField('Емейл', max_length=90, blank=True)
    phone = models.CharField('Телефон', max_length=90, blank=True)
    photo = ThumbnailerImageField(upload_to=photo_upload_to, blank=True)

    class Meta:
        verbose_name_plural = 'initiators'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.first_name} {self.last_name}')
        super().save(*args, **kwargs)
