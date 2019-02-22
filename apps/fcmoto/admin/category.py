import csv
import math

from django.contrib import admin
from django.shortcuts import HttpResponse

from ..models import Product
from ..tasks import category_task


class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""

    def parse(self, request, categories):
        """Run category parser"""
        for category in categories:
            category_task.delay(category_id=category.id)

    parse.short_description = 'Начать парсинг'

    def export_as_csv(self, request, categories):
        """Export csv file"""
        for category in categories:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = "attachment; filename=export_webasyst_{category_id}.csv".format(
                category_id=category.id)
            csv_writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

            # заголовок
            col_names = [
                'Наименование',
                'Наименование артикула',
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
                'Заголовок',
                'META Keywords',
                'META Description',
                'Ссылка на витрину',
                'Производитель',
                'Пол',
                'Размер',
                'Цвет',
                'Изображения',
                'Изображения',
                'Изображения',
                'Изображения',
                'Изображения',
                'Изображения',
            ]
            csv_writer.writerow([item.encode('utf8').decode('utf8') for item in col_names])

            # подзаголовок 1
            col_names = [
                '<Категория>',
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
                '1',
                '',
                '',
                'текст пользователя парсера',
                'текст пользователя парсера',
                'текст пользователя парсера',
                'текст пользователя парсера типа «kategoriya»',
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

            # подзаголовок 1
            col_names = [
                '!подкатегория1',
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
                '1',
                '',
                '',
                'текст пользователя парсера',
                'текст пользователя парсера',
                'текст пользователя парсера',
                'текст пользователя парсера типа «kategoriya1»',
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

            # подзаголовок 2
            col_names = [
                '!подкатегория2',
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
                '1',
                '',
                '',
                'текст пользователя парсера',
                'текст пользователя парсера',
                'текст пользователя парсера',
                'текст пользователя парсера типа «kategoriya2»',
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

            # подзаголовок 3
            col_names = [
                '!подкатегория3',
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
                '1',
                '',
                '',
                'текст пользователя парсера',
                'текст пользователя парсера',
                'текст пользователя парсера',
                'текст пользователя парсера типа «kategoriya3»',
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

            products = category.product_set.filter(status=Product.STATUS_CHOICE_DONE, is_active=True)

            bage_html = '<div class="badge" style="background-color: #ff8c2b;"><span>в Европе</span></div>'

            for product in products:
                counter = 1
                product_list = []
                all_sizes = []
                all_available = 0
                is_main_article = True

                name = product.name
                name_url = product.name_url
                manufacturer = product.manufacturer
                front_picture = product.front_picture
                back_picture = product.back_picture
                price = math.ceil(product.price)
                description_html = product.description_html
                description_text = product.description_text
                sizes = product.attributes.get('sizes', [])
                color_value = product.attributes.get('color', '')
                gender_value = product.category.gender if product.category else ''

                for size in sizes:
                    size_value = size.get('size', '').strip()
                    all_sizes.append(size_value)

                    available_value = 1 if size.get('available', False) else 0
                    all_available += available_value

                    keywords = ", ".join(name.split(' '))

                    if available_value and is_main_article:
                        main_article = 1
                        is_main_article = False
                    else:
                        main_article = 0

                    if counter == 1:
                        item = [
                            name,
                            '{size}, {colors}'.format(size=size_value, colors=color_value).strip(', '),
                            'RUB',
                            price,
                            str(1 if available_value else 0),
                            str(0),
                            price,
                            str(1 if available_value else 0),
                            str(main_article),
                            str(0),
                            str(0),
                            str(1 if available_value else 0),
                            'Купить {}'.format(name),
                            description_html,
                            bage_html,
                            '1',
                            'Одежда',
                            '<{{{keywords}}}>'.format(keywords=keywords).replace('<{}>', ''),
                            name,
                            keywords,
                            description_text,
                            name_url,
                            '',
                            '',
                            str(size_value),
                            str(color_value),
                            front_picture,
                            back_picture,
                        ]
                        product_list.append(item)
                    else:
                        item = [
                            name,
                            '{size}, {colors}'.format(size=size_value, colors=color_value).strip(', '),
                            'RUB',
                            price,
                            str(1 if available_value else 0),
                            str(0),
                            price,
                            str(1 if available_value else 0),
                            str(main_article),
                            str(0),
                            str(0),
                            str(1 if available_value else 0),
                            '',
                            '',
                            bage_html,
                            '1',
                            'Одежда',
                            '',
                            '',
                            '',
                            '',
                            name_url,
                            '',
                            '',
                            str(size_value),
                            str(color_value),
                            '',
                            '',
                        ]
                        product_list.append(item)
                    counter += 1

                # title
                all_size = ",".join(sorted(all_sizes))

                main_item = [
                    name,
                    '',
                    'RUB',
                    price,
                    str(1 if all_available else 0),
                    str(0),
                    price,
                    str(all_available),
                    '',
                    '',
                    '',
                    '',
                    'Купить {}'.format(name),
                    description_html,
                    bage_html,
                    '1',
                    'Одежда',
                    '<{{{keywords}}}>'.format(keywords=keywords).replace('<{}>', ''),
                    name,
                    keywords,
                    description_text,
                    name_url,
                    manufacturer,
                    gender_value,
                    '<{{{all_size}}}>'.format(all_size=all_size).replace('<{}>', ''),
                    '<{{{color}}}>'.format(color=color_value).replace('<{}>', ''),
                    front_picture,
                    back_picture,
                ]
                product_list.insert(0, main_item)
                [csv_writer.writerow(item) for item in product_list]

            return response

    export_as_csv.short_description = 'Выгрузить в csv'

    list_display = ('id', 'name', 'status', 'updated_at',)
    list_filter = ('status',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
    actions = (parse, export_as_csv)
