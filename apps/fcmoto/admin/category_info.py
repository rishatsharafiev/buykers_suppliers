from django.contrib import admin


class CategoryInfoAdmin(admin.ModelAdmin):
    """CategoryInfo admin"""

    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_per_page = 20
