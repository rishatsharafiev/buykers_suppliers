from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""

    list_display = ('id', 'name', 'status', 'created_at', 'updated_at',)
    list_filter = ('status',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
