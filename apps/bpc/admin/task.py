import openpyxl
from decimal import Decimal
from django.contrib import admin

from .inlines import GoodInline
from ..models import Good


class TaskAdmin(admin.ModelAdmin):
    """Task admin"""

    exclude = ()
    inlines = (GoodInline,)

    def save_model(self, request, obj, form, change):
        """Save method"""
        super().save_model(request, obj, form, change)

        book = openpyxl.load_workbook(obj.first_file)
        self.sheet_bicycles(book)

    @staticmethod
    def sheet_bicycles(book):
        """Bicycles sheet parser"""
        sheet = book.get_sheet_by_name('Мотоэкипировка')
        row = 4

        while sheet[f'A{row}'].value != '':
            try:
                count = int(sheet[f'H{row}'].value)
            except ValueError:
                continue

            if count:
                code = sheet[f'A{row}'].value
                vendor_code = sheet[f'B{row}'].value
                nomenclature = sheet[f'C{row}'].value
                nomenclature_group = sheet[f'D{row}'].value
                brand = sheet[f'E{row}'].value
                count = sheet[f'H{row}'].value

                try:
                    wholesale_price = Decimal(sheet[f'I{row}'].value)
                    retail_price = Decimal(sheet[f'J{row}'].value)
                except ValueError:
                    continue

                gender_str = sheet[f'O{row}'].value
                for g_c in Good.GENDER_CHOICES:
                    if gender_str == g_c[1]:
                        gender = g_c[0]
                        break
                else:
                    continue

                good = Good(
                    code=code,
                    vendor_code=vendor_code,
                    nomenclature=nomenclature,
                    nomenclature_group=nomenclature_group,
                    brand=brand,
                    count=count,
                    wholesale_price=wholesale_price,
                    retail_price=retail_price,
                    gender=gender
                )
                good.save()

            row += 1
