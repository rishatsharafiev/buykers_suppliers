from django.contrib import admin

from ..tasks import page_task


class PageAdmin(admin.ModelAdmin):
    """Page admin"""

    def parse(self, request, pages):
        """Run category parser"""
        for page in pages:
            page_task.delay(page_id=page.id)

    parse.short_description = 'Начать парсинг'

    list_display = ('id', 'status', 'category', 'updated_at',)
    list_filter = ('status', 'category__name',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
    actions = (parse,)
