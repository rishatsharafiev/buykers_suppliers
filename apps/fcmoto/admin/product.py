from django.contrib import admin

from ..tasks import product_task


class ProductAdmin(admin.ModelAdmin):
    """Product Admin"""

    def parse(self, request, products):
        """Run category parser"""
        products = list(products)

        recycle = True
        slice_count = 10
        product_ids = []

        while recycle:
            # collect product ids
            for i in range(slice_count):
                try:
                    product_ids.append(products.pop().pk)
                except IndexError:
                    recycle = False
                    break
            # run task
            product_task.delay(product_ids=product_ids)
            product_ids = []

    parse.short_description = 'Начать парсинг'

    actions = (parse,)
    list_display = ('id', 'is_active', 'status', 'category', 'name', 'updated_at', 'name_url', 'price',)
    list_filter = ('status', 'is_active', 'category__name',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
