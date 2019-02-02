import csv

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
                'Код артикула',
                'Валюта',
                'Цена',
                'Доступен для заказа',
                'Зачеркнутая цена',
                'Закупочная цена',
                'В наличии',
                'Основной артикул',
                'В наличии @Склад в Москве',
                'В наличии @Склад в Европе',
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
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '<Ссылка на категорию>',
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
            # подзаголовок 2
            col_names = [
                '<Подкатегория>',
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
                '<Ссылка на подкатегорию>',
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

            products = category.product_set.filter(status=Product.STATUS_CHOICE_DONE)

            for product in products:
                counter = 1
                product_list = []
                all_sizes = []

                sizes = product.attributes['sizes']
                for size in sizes:
                    all_sizes.append(size['size'])
                    keywords = ", ".join(product.name.split(' '))

                    if counter == 1:
                        item = [
                            product.name,
                            '{size}, {color}'.format(size=size['size'], color=product.attributes['color']).strip(', '),
                            '',
                            'RUB',
                            product.price,
                            1 if size['available'] else 0,
                            '0',
                            product.price,
                            1 if size['available'] else 0,
                            '',
                            '0',
                            1 if size['available'] else 0,
                            'Купить {}'.format(product.name),
                            product.description_html,
                            '',
                            '1',
                            'Одежда',
                            keywords,
                            '',
                            product.name,
                            keywords,
                            product.description_text,
                            product.name_url,
                            '',
                            '',
                            product.manufacturer,
                            product.manufacturer,
                            '',
                            '',
                            '',
                            '',
                            '{colors}'.format(colors=product.attributes['color']),
                            '',
                            '',
                            '',
                            '',
                            size['size'],
                            product.front_picture,
                            product.back_picture,
                        ]
                        product_list.append(item)

                    elif len(sizes) == counter:
                        all_size = ",".join(sorted(all_sizes))
                        # available_order = sum([(size['size'] if size['available'] else 1) for size in sizes])

                        main_item = [
                            product.name,
                            '',
                            '',
                            'RUB',
                            product.price,
                            '',  # available_order,
                            '0',
                            product.price,
                            '',  # available_order,
                            '',
                            '0',
                            '',  # available_order,
                            'Купить {}'.format(product.name),
                            product.description_html,
                            '',
                            '1',
                            'Одежда',
                            keywords,
                            '',
                            product.name,
                            keywords,
                            product.description_text,
                            product.name_url,
                            '',
                            '',
                            product.manufacturer,
                            product.manufacturer,
                            '',
                            '',
                            '',
                            '',
                            '<{{{color}}}>'.format(color=product.attributes['color']).replace('<{}>', ''),
                            '',
                            '',
                            '',
                            '',
                            '<{{{all_size}}}>'.format(all_size=all_size).replace('<{}>', ''),
                            product.front_picture,
                            product.back_picture,
                        ]
                        product_list.insert(0, main_item)
                    else:
                        item = [
                            product.name,
                            '{size}, {color}'.format(size=size['size'], color=product.attributes['color']).strip(', '),
                            '',
                            'RUB',
                            product.price,
                            1 if size['available'] else 0,
                            '0',
                            product.price,
                            1 if size['available'] else 0,
                            '',
                            '0',
                            1 if size['available'] else 0,
                            'Купить {}'.format(product.name),
                            product.description_html,
                            '',
                            '1',
                            'Одежда',
                            keywords,
                            '',
                            product.name,
                            keywords,
                            product.description_text,
                            product.name_url,
                            '',
                            '',
                            product.manufacturer,
                            product.manufacturer,
                            '',
                            '',
                            '',
                            '',
                            '{color}'.format(color=product.attributes['color']),
                            '',
                            '',
                            '',
                            '',
                            product.attributes['color'],
                            '',
                            '',
                        ]
                        product_list.append(item)
                    counter += 1

                [csv_writer.writerow(item) for item in product_list]

            return response

    export_as_csv.short_description = 'Выгрузить в csv'

    list_display = ('id', 'name', 'status', 'updated_at',)
    list_filter = ('status',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
    actions = (parse, export_as_csv)
