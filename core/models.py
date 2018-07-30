from django.db import models
from django.utils import timezone

from model_utils.fields import AutoLastModifiedField


class BaseModel(models.Model):
    """Base TimeModel"""

    created = models.DateTimeField('Створено', default=timezone.now)
    modified = AutoLastModifiedField('Змінено')
    slug = models.SlugField('Посилання', unique=True, max_length=512)

    class Meta:
        abstract = True
        ordering = ('-created',)
