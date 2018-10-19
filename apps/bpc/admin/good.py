import csv

from django.contrib import admin
from django.http import HttpResponse

from .inlines import PictureInline


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
            'Дотупен для заказа',
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
            'Произовдитель',
            'Бренд',
            'Подходящие модели автомобилей',
            'Вес',
            'Страна происхждения',
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
            size = obj.vendor_code.split('-')[-1]
            description = f"""
            <p><del></del>{obj.descriptions.split()[0]}</p>

            <p>ОСОБЕННОСТИ</p>

            <p>{obj.descriptions.split()[-1]}<del></del></p>
            """

            writer.writerow((
                obj.nomenclature,
                'Наименование артикула',
                obj.vendor_code,
                'Валюта',
                obj.retail_price,
                'Дотупен для заказа',
                'Зачеркнутая цена',
                obj.wholesale_price,
                'В наличии @шоу-рум в Москве (в наличии)',
                'В наличии @склад в Москве (1-2 дня)',
                'В наличии @cклад в Европе (около 10 дней)',
                f'Купить {obj.nomenclature}',
                description,
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
                obj.brand.lower(),
                obj.brand.lower(),
                'Подходящие модели автомобилей',
                'Вес',
                'Страна происхждения',
                obj.gender,
                'Цвет',
                'Материал',
                'Материал подошвы',
                'Уровень',
                'Максимальный вес пользователя',
                size,
                'Изображения',
                'Изображения',
                'Изображения',
                'Изображения',
                'Изображения',
            ))

        return response

    export_as_csv.short_description = "Выгрузить в csv"

    search_fields = ('code', 'vendor_code')
    actions = (export_as_csv,)
    exclude = ()
    list_filter = ('task', 'nomenclature_group', 'brand', 'gender')
    list_display = ('task', 'code', 'vendor_code', 'nomenclature_group', 'brand', 'wholesale_price', 'retail_price')
    inlines = (PictureInline,)
