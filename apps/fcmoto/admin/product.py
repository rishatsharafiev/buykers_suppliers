from math import ceil

from django.contrib import admin

from ..models import Product
from ..tasks import product_task


class ProductAdmin(admin.ModelAdmin):
    """Product Admin"""

    def parse(self, request, products):
        """Run category parser"""
        all_product_ids = [product.id for product in products.exclude(status=Product.STATUS_CHOICE_DONE)]
        products_per_task = 10

        for pos in range(int(ceil(len(all_product_ids) / products_per_task))):
            group_ids = all_product_ids[pos * products_per_task:pos * products_per_task + products_per_task]
            product_task.delay(product_ids=group_ids)

    parse.short_description = "Начать парсинг"

    actions = (parse,)
    list_display = ('id', 'status', 'category', 'link', 'name', 'name_url', 'price')
    list_filter = ('status', 'category')
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at')
