from django.contrib import admin

from .inlines import PictureInline


class GoodAdmin(admin.ModelAdmin):
    """Good admin"""

    exclude = ()
    list_filter = ('task', 'nomenclature_group', 'brand', 'gender')
    list_display = ('task', 'code', 'vendor_code', 'nomenclature_group', 'brand', 'wholesale_price', 'retail_price')
    inlines = (PictureInline,)
