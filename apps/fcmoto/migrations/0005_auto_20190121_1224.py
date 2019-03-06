# Generated by Django 2.1.5 on 2019-01-21 09:24

from django.db import migrations, models
import django.db.models.deletion
import jsoneditor.fields.postgres_jsonfield


class Migration(migrations.Migration):

    dependencies = [
        ('fcmoto', '0004_auto_20190116_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NEW', 'Новый'), ('PROGRESS', 'В обработке'), ('DONE', 'Закончен'), ('ERROR', 'Ошибка')], default='NEW', max_length=255, verbose_name='Статус')),
                ('page_url', models.TextField(verbose_name='Ссылка на страницу')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcmoto.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(blank=True, null=True, verbose_name='Атрибуты'),
        ),
    ]