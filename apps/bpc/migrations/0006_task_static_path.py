# Generated by Django 2.1.1 on 2018-10-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpc', '0005_auto_20181013_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='static_path',
            field=models.CharField(default='/wa-data/public/site/import', max_length=255, verbose_name='Путь до папки с изображениями'),
        ),
    ]
