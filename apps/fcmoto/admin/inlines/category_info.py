from django.contrib import admin

from ...models import CategoryInfo


class CategoryInfoInlineAdmin(admin.TabularInline):
    """CategoryInfo Inline Admin"""

    model = CategoryInfo
    extra = 1
    ordering = ('order',)
