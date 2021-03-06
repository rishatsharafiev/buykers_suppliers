# Generated by Django 2.1.5 on 2019-02-12 06:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fcmoto', '0005_auto_20190121_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 2, 12, 6, 30, 10, 885608, tzinfo=utc), verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
    ]
