# Generated by Django 2.1.5 on 2019-01-16 10:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcmoto', '0003_auto_20190116_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='back_picture',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator], verbose_name='Задний план'),
        ),
        migrations.AlterField(
            model_name='product',
            name='front_picture',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator], verbose_name='Передний план'),
        ),
    ]
