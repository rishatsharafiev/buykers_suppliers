import openpyxl
import logging
import decimal
from django.contrib import admin
from django.db import transaction

from conf import settings

from .inlines import GoodInline
from ..models import Good


class TaskAdmin(admin.ModelAdmin):
    """Task admin"""

    exclude = ()
    inlines = (GoodInline,)

    def save_model(self, request, obj, form, change):
        """Save method"""
        super().save_model(request, obj, form, change)
        file_path = settings.MEDIA_ROOT / str(obj.first_file)
        logging.error(file_path)
        workbook = openpyxl.load_workbook(filename=file_path, read_only=True)
        self.save_motos(obj, workbook)

    def save_motos(self, task, workbook):
        """Bicycles sheet parser"""
        worksheet = workbook['Мотоэкипировка']
        counter = 0

        genders = list(zip(*Good.GENDER_CHOICES))
        genders_indexes = genders[0]
        genders_titles = genders[1]

        with transaction.atomic():
            for row in worksheet.iter_rows(row_offset=3):
                code = row[0].value
                vendor_code = row[1].value
                nomenclature = row[2].value
                nomenclature_group = row[3].value
                brand = row[4].value
                try:
                    count = int(row[5].value)
                    wholesale_price = decimal.Decimal(row[8].value)
                    retail_price = decimal.Decimal(row[9].value)
                except (ValueError, TypeError, decimal.InvalidOperation):
                    continue
                try:
                    gender_index = genders_titles.index(row[14].value)
                    gender = genders_indexes[gender_index]
                except ValueError:
                    gender = Good.GENDER_EMPTY_CHOICE

                good = Good(
                    code=code,
                    vendor_code=vendor_code,
                    nomenclature=nomenclature,
                    nomenclature_group=nomenclature_group,
                    brand=brand,
                    count=count,
                    wholesale_price=wholesale_price,
                    retail_price=retail_price,
                    gender=gender,
                    task=task,
                )
                good.save()

