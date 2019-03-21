import csv
import math

from django.contrib import admin
from django.shortcuts import HttpResponse

from .inlines import CategoryInfoInlineAdmin
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

            # # подзаголовок 1
            # col_names = [
            #     '<Категория>',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '1',
            #     '',
            #     '',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера типа «kategoriya»',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            # ]
            # csv_writer.writerow([item.encode('utf8').decode('utf8') for item in col_names])
            #
            # # подзаголовок 1
            # col_names = [
            #     '!подкатегория1',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '1',
            #     '',
            #     '',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера типа «kategoriya1»',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            # ]
            # csv_writer.writerow([item.encode('utf8').decode('utf8') for item in col_names])
            #
            # # подзаголовок 2
            # col_names = [
            #     '!подкатегория2',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '1',
            #     '',
            #     '',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера типа «kategoriya2»',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            # ]
            # csv_writer.writerow([item.encode('utf8').decode('utf8') for item in col_names])
            #
            # # подзаголовок 3
            # col_names = [
            #     '!подкатегория3',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '1',
            #     '',
            #     '',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера',
            #     'текст пользователя парсера типа «kategoriya3»',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            #     '',
            # ]
            # csv_writer.writerow([item.encode('utf8').decode('utf8') for item in col_names])

            products = category.product_set.filter(status=Product.STATUS_CHOICE_DONE, is_active=True)\
                .distinct('name_url_color')

            bage_html = '<div class="badge" style="background-color: #ff8c2b;"><span>в Европе</span></div>'

            category_margin = category.margin if category.margin else 0
            category_delivery = category.delivery if category.delivery else 0

            # category info
            category_info_rows = category.categoryinfo_set.order_by('order')

            for category_info in category_info_rows:
                item = [
                    category_info.name,
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
                    category_info.title,
                    category_info.meta_keywords,
                    category_info.meta_description,
                    category_info.link,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                ]
                csv_writer.writerow(item)

            for product in products:
                counter = 1
                product_list = []
                all_sizes = []
                all_available = 0
                is_main_article = True

                name = product.name
                name_url_color = product.name_url_color
                manufacturer = product.manufacturer
                front_picture = product.front_picture
                back_picture = product.back_picture
                purchase_price = math.ceil(product.price)
                online_price = math.ceil(purchase_price + purchase_price * category_margin / 100 + category_delivery)
                description_html = product.description_html
                description_text = product.description_text
                sizes = product.attributes.get('sizes', [])
                color_value = product.attributes.get('color', '')
                gender_value = product.category.gender if product.category else ''
                keywords = ", ".join(name.split(' '))

                for size in sizes:
                    size_value = size.get('size', '').strip()
                    all_sizes.append(size_value)

                    available_value = 1 if size.get('available', False) else 0
                    all_available += available_value

                    available_value = available_value if product.is_active else 0

                    if available_value and is_main_article:
                        main_article = str(1)
                        is_main_article = False
                    else:
                        main_article = ''

                    if counter == 1:
                        item = [
                            name,
                            '{size}, {colors}'.format(size=size_value, colors=color_value).strip(', '),
                            'RUB',
                            online_price,
                            str(1 if available_value else 0),
                            str(0),
                            purchase_price,
                            str(1 if available_value else 0),
                            main_article,
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
                            name_url_color,
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
                            online_price,
                            str(1 if available_value else 0),
                            str(0),
                            purchase_price,
                            str(1 if available_value else 0),
                            main_article,
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
                            name_url_color,
                            '',
                            '',
                            str(size_value),
                            str(color_value),
                            '',
                            '',
                        ]
                        product_list.append(item)
                    counter += 1

                all_available = all_available if product.is_active else 0

                # title
                all_size = ",".join(sorted(all_sizes))

                main_item = [
                    name,
                    '',
                    'RUB',
                    online_price,
                    str(1 if all_available else 0),
                    str(0),
                    purchase_price,
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
                    name_url_color,
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
    inlines = [CategoryInfoInlineAdmin, ]
