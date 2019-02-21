from decimal import Decimal

from django.db import models


class Category(models.Model):
    """Category model"""

    STATUS_CHOICE_NEW = 'NEW'
    STATUS_CHOICE_PROGRESS = 'PROGRESS'
    STATUS_CHOICE_DONE = 'DONE'
    STATUS_CHOICE_ERROR = 'ERROR'

    STATUS_CHOICES = (
        (STATUS_CHOICE_NEW, 'Новый'),
        (STATUS_CHOICE_PROGRESS, 'В обработке'),
        (STATUS_CHOICE_DONE, 'Закончен'),
        (STATUS_CHOICE_ERROR, 'Ошибка')
    )

    status = models.CharField(verbose_name='Статус', max_length=255, choices=STATUS_CHOICES, default=STATUS_CHOICE_NEW)
    name = models.CharField(verbose_name='Наименование', max_length=255)
    link = models.URLField(verbose_name='Ссылка на категорию')

    gender = models.CharField(verbose_name='Пол', max_length=255, default='')
    margin = models.DecimalField(verbose_name='Наценка (%)', decimal_places=2, max_digits=12, default=Decimal(0))
    delivery = models.DecimalField(verbose_name='Доставка', decimal_places=2, max_digits=12, default=Decimal(0))

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        """Meta"""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'
