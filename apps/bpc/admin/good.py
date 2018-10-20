import csv
import re

import transliterate
from django.contrib import admin
from django.http import HttpResponse

from .inlines import PictureInline
from ..models import Good, Picture


class GoodAdmin(admin.ModelAdmin):
    """Good admin"""

    def export_as_csv(self, request, queryset):
        """Export csv file"""
        meta = self.model._meta

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow((
            'Наименование',
            'Наименование артикула',
            'Код артикула',
            'Валюта',
            'Цена',
            'Доступен для заказа',
            'Зачеркнутая цена',
            'Закупоная цена',
            'В наличии @шоу-рум в Москве (в наличии)',
            'В наличии @склад в Москве (1-2 дня)',
            'В наличии @cклад в Европе (около 10 дней)',
            'Краткое описание',
            'Описание',
            'Наклейка',
            'Статус',
            'Тип товара',
            'Теги',
            'Облагается налогом',
            'Заголовок',
            'META Keywords',
            'META Description',
            'Ссылка на ветрину',
            'Адрес видео на YouTube или Vimeo',
            'Дополнительные параметры',
            'Производитель',
            'Бренд',
            'Подходящие модели автомобилей',
            'Вес',
            'Страна происхождения',
            'Пол',
            'Цвет',
            'Материал',
            'Материал подошвы',
            'Уровень',
            'Максимальный вес пользователя',
            'Размер',
            'Изображения',
            'Изображения',
            'Изображения',
            'Изображения',
            'Изображения',
        ))

        for obj in queryset:
            pictures = Picture.objects.filter(good=obj)
            size = obj.vendor_code.split('-')[-1]

            # Size
            t = re.compile(r'([\w\d/]+)$')
            v_code_name = t.search(obj.vendor_code).group(0) if t.search(obj.vendor_code).group(0) else ''

            # link
            tr = transliterate.translit(obj.nomenclature.replace('(', '').replace(')', ''), reversed=True)
            link = '-'.join([w for w in tr.split()])

            # Gender
            genders = list(zip(*Good.GENDER_CHOICES))
            genders_indexes = genders[0]
            genders_titles = genders[1]
            t_index = genders_indexes.index(obj.gender)
            gender = genders_titles[t_index]

            writer.writerow((
                obj.nomenclature,
                v_code_name,
                obj.vendor_code,
                'RUB',  # Можно парсить из второго файла, в бд пока не предусмотренно
                obj.retail_price,
                '1',
                '',
                obj.wholesale_price,
                '',
                '',
                '',
                f'Купить {obj.nomenclature}',
                obj.descriptions,
                '',
                '1',
                '',
                '',
                '',
                obj.nomenclature,
                ', '.join([a for a in obj.nomenclature.split()[:-1]]),
                f'Купить {obj.nomenclature}',
                link,  # Ссылка на ветрину
                '',
                '',
                obj.brand.lower(),
                obj.brand.lower(),
                '',
                '',
                '',
                gender,
                '',
                '',
                '',
                '',
                '',
                size,
                pictures.get(name__contains='_1') if pictures.filter(name__contains='_1') else '',
                pictures.get(name__contains='_2') if pictures.filter(name__contains='_1') else '',
                pictures.get(name__contains='_3') if pictures.filter(name__contains='_1') else '',
                pictures.get(name__contains='_4') if pictures.filter(name__contains='_1') else '',
                pictures.get(name__contains='_5') if pictures.filter(name__contains='_1') else '',
            ))

        return response

    export_as_csv.short_description = "Выгрузить в csv"

    search_fields = ('code', 'vendor_code')
    actions = (export_as_csv,)
    exclude = ()
    list_filter = ('task', 'nomenclature_group', 'brand', 'gender')
    list_display = ('task', 'code', 'vendor_code', 'nomenclature_group', 'brand', 'wholesale_price', 'retail_price')
    inlines = (PictureInline,)
