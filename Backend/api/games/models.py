from django.db import models
from django.core.exceptions import ValidationError

from .constants import MEGABYTE_IMAGE_SIZE_LIMIT


class GamesModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.FloatField()
    score = models.IntegerField()
    image = models.ImageField()

    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > MEGABYTE_IMAGE_SIZE_LIMIT * 1024 * 1024:
                raise ValidationError(f'Image size must be no more than {MEGABYTE_IMAGE_SIZE_LIMIT} MB')
            if '<script>' in self.image.name.lower() or '</script>' in self.image.name.lower():
                raise ValidationError(f'Xss Attack')
            if '<script>' in self.name.lower() or '</script>' in self.image.name.lower():
                raise ValidationError(f'Xss Attack')
        super().save(*args, **kwargs)
