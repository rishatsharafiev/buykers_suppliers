from django.contrib import admin

from ...models import CategoryInfo


class CategoryInfoInlineAdmin(admin.StackedInline):
    """CategoryInfo Inline Admin"""

    model = CategoryInfo
    extra = 0
    ordering = ('order',)
