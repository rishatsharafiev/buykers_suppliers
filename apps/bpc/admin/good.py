import csv
import re

import transliterate
from django.contrib import admin
from django.http import HttpResponse

from .inlines import PictureInline
from ..models import Good


class GoodAdmin(admin.ModelAdmin):
    """Good admin"""

    def export_as_csv(self, request, goods):
        """Export csv file"""
        meta = self.model._meta

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        csv_writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

        # заголовок
        col_names = [
            'Наименование',
            'Наименование артикула',
            'Код артикула',
            'Валюта',
            'Цена',
            'Доступен для заказа',
            'Зачеркнутая цена',
            'Закупочная цена',
            'В наличии',
            'Основной артикул',
            'В наличии @шоу-рум в Москве (в наличии)',
            'В наличии @склад в Москве (1-2 дня)',
            'В наличии @cклад в Европе (около 10 дней)',
            'Краткое описание',
            'Описание',
            'Наклейка',
            'Статус',
            'Тип товаров',
            'Теги',
            'Облагается налогом',
            'Заголовок',
            'META Keywords',
            'META Description',
            'Ссылка на витрину',
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
        ]

        csv_writer.writerow([item.encode('utf8').decode('utf8') for item in col_names])

        for good in goods:
            # size = good.vendor_code.split('-')[-1]
            #
            # # Size
            # t = re.compile(r'([\w\d/]+)$')
            # v_code_name = t.search(good.vendor_code).group(0) if t.search(good.vendor_code).group(0) else ''

            # link
            tr = transliterate.translit(good.nomenclature.replace('(', '').replace(')', ''), reversed=True)
            link = '-'.join([w for w in tr.split()])

            # Gender
            genders = list(zip(*Good.GENDER_CHOICES))
            genders_titles = genders[1]
            try:

                if good.gender == Good.GENDER_TEEN_CHOICE:
                    gender = genders_titles[Good.GENDER_CHILD_CHOICE]
                else:
                    gender = genders_titles[good.gender]
            except ValueError:
                gender = ''

            pictures = good.picture_set.all()[:5]

            items = [
                good.nomenclature,
                '',
                good.vendor_code,
                'RUB',
                str(good.retail_price).replace('.', ','),
                '1',
                '0',
                str(good.wholesale_price).replace('.', ','),
                '1',
                '',
                '',
                '',
                '',
                f'Купить {good.nomenclature}',
                good.descriptions,
                '',
                '1',
                good.nomenclature_group,
                '',
                '',
                good.nomenclature,
                ', '.join([a for a in good.nomenclature.split()[:-1]]),
                f'Купить {good.nomenclature}',
                link,  # Ссылка на ветрину
                '',
                '',
                good.brand.lower(),
                good.brand.lower(),
                '',
                '',
                '',
                gender,
                '',
                '',
                '',
                '',
                '',
                '<{один размер}>',
            ]
            items.extend([f'{good.task.static_path}/{picture.name}' for picture in pictures])

            csv_writer.writerow([item.encode('utf8').decode('utf8') for item in items])

            items = [
                good.nomenclature,
                '',
                good.vendor_code,
                'RUB',
                str(good.retail_price).replace('.', ','),
                '1',
                '0',
                str(good.wholesale_price).replace('.', ','),
                '1',
                '1',
                '0',
                '1',
                '0',
                f'Купить {good.nomenclature}',
                good.descriptions,
                '',
                '1',
                good.nomenclature_group,
                '',
                '',
                good.nomenclature,
                ', '.join([a for a in good.nomenclature.split()[:-1]]),
                f'Купить {good.nomenclature}',
                link,  # Ссылка на ветрину
                '',
                '',
                good.brand.lower(),
                good.brand.lower(),
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                'один размер',
            ]
            items.extend([f'{good.task.static_path}/{picture.name}' for picture in pictures])

            csv_writer.writerow([item.encode('utf8').decode('utf8') for item in items])

            # write ending row
            col_names = [
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
            ]
            csv_writer.writerow([item.encode('utf8').decode('utf8') for item in col_names])

        return response

    export_as_csv.short_description = "Выгрузить в csv"

    search_fields = ('code', 'vendor_code')
    actions = (export_as_csv,)
    exclude = ()
    list_filter = ('task', 'nomenclature_group', 'brand', 'gender')
    list_display = ('code', 'task', 'vendor_code', 'nomenclature_group', 'brand', 'wholesale_price', 'retail_price')
    inlines = (PictureInline,)
