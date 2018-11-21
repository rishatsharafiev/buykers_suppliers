from django.contrib import admin
from ..parsers import TaskParser


class TaskAdmin(admin.ModelAdmin):
    """Task admin"""

    exclude = ()
    # inlines = (GoodInline,)

    def save_model(self, request, obj, form, change):
        """Save method"""
        super().save_model(request, obj, form, change)

        TaskParser().run(obj)
