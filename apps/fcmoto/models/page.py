from django.db import models

from .category import Category


class Page(models.Model):
    """Page model"""

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
    page_url = models.TextField(verbose_name='Ссылка на страницу')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        """Meta"""

        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        try:
            return f"{self.category.name} {self.page_url.rsplit('=', 1)[1]}"
        except IndexError:
            return f"{self.category.name}"
