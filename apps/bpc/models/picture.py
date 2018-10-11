from django.db import models

from .good import Good


class Picture(models.Model):
    """Picture model"""

    name = models.CharField(verbose_name='Название', max_length=128)
    good = models.ForeignKey(Good, verbose_name='Товар', on_delete=models.CASCADE)

    class Meta:
        """Meta"""

        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.name
