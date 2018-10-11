from django.contrib import admin

from ...models.good import Good


class GoodInline(admin.TabularInline):
    """Picture inline"""

    model = Good
    fields = ('code', 'vendor_code', 'wholesale_price', 'retail_price')
