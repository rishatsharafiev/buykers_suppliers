# Generated by Django 2.1.5 on 2019-01-16 05:56

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('AVAILABLE', 'В наличии'), ('NOT_AVAILABLE', 'Нет в наличии')], default='AVAILABLE', max_length=255, verbose_name='Статус')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('link', models.URLField(verbose_name='Ссылка на категорию')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NEW', 'Новый'), ('PROGRESS', 'В обработке'), ('DONE', 'Закончен'), ('ERROR', 'Ошибка')], default='NEW', max_length=255, verbose_name='Статус')),
                ('link', models.URLField(max_length=255, verbose_name='Ссылка для сбора')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('producer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Производитель')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Цена по прайсу')),
                ('retail_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Цена в магазинах сети')),
                ('online_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Цена в интернет-магазине')),
                ('special_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Цена товара недели')),
                ('model', models.CharField(blank=True, max_length=255, null=True, verbose_name='Модель')),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Атрибуты')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcmoto.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('category', 'producer', 'model'),
            },
        ),
    ]
