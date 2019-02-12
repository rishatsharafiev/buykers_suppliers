from django.contrib import admin

from ..tasks import category_task


class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""

    def parse(self, request, categories):
        """Run category parser"""
        for category in categories:
            category_task.delay(category_id=category.id)

    parse.short_description = 'Начать парсинг'

    list_display = ('id', 'name', 'status', 'updated_at',)
    list_filter = ('status',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
    actions = (parse,)
