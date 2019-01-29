from django.contrib import admin

from ..tasks import page_task


class PageAdmin(admin.ModelAdmin):
    """Page admin"""

    def parse(self, request, pages):
        """Run category parser"""
        for page in pages:
            page_task.delay(page_id=page.id)

    parse.short_description = "Начать парсинг"

    actions = (parse,)
    list_per_page = 20
