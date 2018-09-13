import random

from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from model_utils import Choices
from easy_thumbnails.fields import ThumbnailerImageField
from transliterate import slugify

from core.mixins import FileDownloadCommandMixin
from core.models import BaseModel
from committees.models import Committee
from initiators.managers import InitiatorManager


def photo_upload_to(instance, filename):
    extension = filename.split('.')[-1]
    return (f'initiators/{instance.first_name}_{instance.last_name}'
            + f'/{instance.slug}' + '.' + extension)


class Convocation(BaseModel):
    """Store information about convocations."""

    CONVOCATION = Choices((8, 'VIII', 'VIII скликання'))

    number = models.PositiveSmallIntegerField('Конвокація',
        choices=CONVOCATION, unique=True, null=True, blank=True)
    latin_number = models.CharField('Конвокація (лат.)', max_length=25,
                                   blank=True)
    slug = models.SlugField('Посилання', unique=True, max_length=90,
                            null=True)

    def __str__(self):
        return f'{self.latin_number}'


class Initiator(FileDownloadCommandMixin, BaseModel):
    """Store information about initiators of bills."""

    CONVOCATION = Choices((8, 'VIII', 'VIII скликання'))

    first_name = models.CharField("Ім'я", max_length=50)
    last_name = models.CharField('Прізвище', max_length=100)
    middle_name = models.CharField('По батькові', max_length=100,
                                   blank=True)
    post = models.CharField('Посада', max_length=90, blank=True)
    organization = models.CharField('Організація', max_length=90, blank=True)
    rada_id = models.PositiveSmallIntegerField(unique=True, null=True,
                                              blank=True)
    person_id = models.PositiveSmallIntegerField(unique=True, null=True,
                                                 blank=True)
    party = models.CharField('Партія', max_length=200, blank=True)
    faction = models.CharField('Фракція', max_length=200, blank=True)
    information = models.CharField('Інформація', max_length=2000, blank=True)
    email = models.EmailField('Емейл', max_length=90, blank=True)
    phone = models.CharField('Телефон', max_length=90, blank=True)
    photo = ThumbnailerImageField(upload_to=photo_upload_to, blank=True)
    convocations = models.ManyToManyField(Convocation,
                                         related_name='initiators', blank=True)
    committees = models.ManyToManyField(Committee, related_name='initiators',
                                        blank=True)

    objects = models.Manager()
    objects = InitiatorManager()

    class Meta:
        verbose_name_plural = 'initiators'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.first_name} {self.last_name}')
        super().save(*args, **kwargs)

    def save_photo(self, photo_url):
        """Save initiator's photo."""

        r = self.download_file(photo_url)
        if r and r.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(r.content)
            img_temp.flush()
            filename = photo_url.split('/')[-1]
            self.photo.save(filename, File(img_temp))
        return None
