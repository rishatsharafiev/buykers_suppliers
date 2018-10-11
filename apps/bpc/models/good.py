from django.db import models

from .task import Task


class Good(models.Model):
    """Goog model"""

    GENDER_MAN_CHOICE = 0
    GENDER_WOMAN_CHOICE = 1
    GENDER_CHOICES = (
        (GENDER_MAN_CHOICE, 'Мужской'),
        (GENDER_WOMAN_CHOICE, 'Женский'),
    )

    nomenclature = models.CharField(verbose_name='Номенклатура', max_length=255)
    brand = models.CharField(verbose_name='Бренд', max_length=64)
    code = models.CharField(verbose_name='Код', max_length=32, unique=True)
    vendor_code = models.CharField(verbose_name='Артикул', max_length=32)
    nomenclature_group = models.CharField(verbose_name='Номенклатурная группа', max_length=32)
    count = models.PositiveIntegerField(verbose_name='Количество')
    wholesale_price = models.DecimalField(verbose_name='Оптовая цена', max_digits=8, decimal_places=2)
    retail_price = models.DecimalField(verbose_name='Розничная цена', max_digits=8, decimal_places=2)
    gender = models.PositiveIntegerField(verbose_name='Пол', choices=GENDER_CHOICES)
    descriptions = models.TextField(verbose_name='Описание', null=True, blank=True)
    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE)

    class Meta:
        """Meta"""

        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.code} {self.vendor_code} {self.nomenclature}'
