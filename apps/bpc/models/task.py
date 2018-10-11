import uuid

from django.db import models


def get_file_path(_, filename):
    """Get file path of first file"""
    extension = filename.split('.')[-1]
    id = uuid.uuid4()
    return f'bpc/{id}.{extension}'


class Task(models.Model):
    """Task model"""

    STATUS_CHOICE_NEW = 0
    STATUS_CHOICE_PROGRESS = 1
    STATUS_CHOICE_DONE = 2
    STATUS_CHOICE_ERROR = 3

    STATUS_CHOICES = (
        (STATUS_CHOICE_NEW, 'Новый'),
        (STATUS_CHOICE_PROGRESS, 'В обработке'),
        (STATUS_CHOICE_DONE, 'Закончен'),
        (STATUS_CHOICE_ERROR, 'Ошибка')
    )

    name = models.CharField(verbose_name='Название', max_length=128)
    first_file = models.FileField(verbose_name='Первый файл(xlsx)', upload_to=get_file_path)
    second_file = models.FileField(verbose_name='Второй файл(xlsx)', upload_to=get_file_path)
    zip_file = models.FileField(verbose_name='Zip файл', upload_to=get_file_path)

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    status = models.PositiveIntegerField(verbose_name='Статус',
                                         choices=STATUS_CHOICES,
                                         default=STATUS_CHOICE_NEW)

    class Meta:
        """Meta"""

        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name
