from django.db import models

from .category import Category


class CategoryInfo(models.Model):
    """Category Info model"""

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)

    order = models.PositiveIntegerField(verbose_name='Порядок')
    name = models.CharField(verbose_name='Наименование', max_length=255)
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    meta_keywords = models.CharField(verbose_name='META Keywords', max_length=255)
    meta_description = models.TextField(verbose_name='META Description')
    link = models.URLField(verbose_name='Ссылка на витрину', max_length=255)

    class Meta:
        """Meta"""

        verbose_name = 'Категория - информация'
        verbose_name_plural = 'Категории - информация'

    def __str__(self):
        return f'{self.name}'
