from django.db import models


class Task(models.Model):
    """Task model"""

    name = models.CharField(verbose_name='Название', max_length=128)
    first_file = models.FileField(verbose_name='Первый файл(excel)')
    second_file = models.FileField(verbose_name='Второй файл(excel)')
    zip_file = models.FileField(verbose_name='Zip файл')
    picture_path = models.FilePathField(verbose_name='Путь до изображений')

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        """Meta"""

        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name
