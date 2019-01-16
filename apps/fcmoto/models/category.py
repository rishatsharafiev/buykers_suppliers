from django.db import models


class Category(models.Model):
    """Category model"""

    STATUS_CHOICE_AVAILABLE = 'AVAILABLE'
    STATUS_CHOICE_NOT_AVAILABLE = 'NOT_AVAILABLE'

    STATUS_CHOICES = (
        (STATUS_CHOICE_AVAILABLE, 'В наличии'),
        (STATUS_CHOICE_NOT_AVAILABLE, 'Нет в наличии')
    )
    status = models.CharField(verbose_name='Статус', max_length=255, choices=STATUS_CHOICES,
                              default=STATUS_CHOICE_AVAILABLE)
    name = models.CharField(verbose_name='Наименование', max_length=255)
    link = models.URLField(verbose_name='Ссылка на категорию')

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        """Meta"""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'${self.name}'
