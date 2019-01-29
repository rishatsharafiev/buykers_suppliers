from django.contrib import admin

from ..parsers import ProductParser


class ProductAdmin(admin.ModelAdmin):
    """Product Admin"""

    def parse(self, request, queryset):
        """Run category parser"""
        ids = [obj.id for obj in queryset]
        ProductParser().run(ids)

    parse.short_description = "Начать парсинг"

    actions = (parse,)
    list_display = ('id', 'status', 'category', 'link', 'name', 'name_url', 'price')
    list_filter = ('status', 'category',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
