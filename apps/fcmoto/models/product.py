from django.core.validators import URLValidator
from django.db import models
from jsoneditor.fields.postgres_jsonfield import JSONField

from .category import Category
from .page import Page


class Product(models.Model):
    """Product model"""

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
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    page = models.ForeignKey(Page, verbose_name='Страница', on_delete=models.SET_NULL, blank=True, null=True)
    link = models.TextField(verbose_name='Ссылка для сбора')
    name = models.CharField(verbose_name='Название', max_length=255, blank=True, null=True)
    name_url = models.CharField(verbose_name='Название url', max_length=255, blank=True, null=True)
    front_picture = models.TextField(verbose_name='Передний план', validators=[URLValidator], blank=True, null=True)
    back_picture = models.TextField(verbose_name='Задний план', validators=[URLValidator], blank=True, null=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2,
                                blank=True, null=True)
    attributes = JSONField(verbose_name='Атрибуты', blank=True, null=True)  # colors, sizes
    description_html = models.TextField(verbose_name='Html описание', blank=True, null=True)
    description_text = models.TextField(verbose_name='Текстовое описание', blank=True, null=True)
    manufacturer = models.CharField(verbose_name='Производитель', max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        """Meta"""

        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name}"
