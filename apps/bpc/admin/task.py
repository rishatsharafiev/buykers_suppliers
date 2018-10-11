from django.contrib import admin


class TaskAdmin(admin.ModelAdmin):
    """Task admin"""

    exclude = ()
