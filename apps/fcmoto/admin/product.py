from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    """Product Admin"""

    list_display = ('id', 'status', 'category', 'link', 'name', 'name_url', 'price')
    list_filter = ('status', 'category',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at', )
