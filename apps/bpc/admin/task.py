from django.contrib import admin

from .inlines import GoodInline


class TaskAdmin(admin.ModelAdmin):
    """Task admin"""

    exclude = ()
    inlines = (GoodInline,)
