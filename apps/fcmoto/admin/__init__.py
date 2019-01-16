"""Admin"""

from django.contrib import admin

from .category import CategoryAdmin

from ..models import (
    Product,
    Category
)


admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)
