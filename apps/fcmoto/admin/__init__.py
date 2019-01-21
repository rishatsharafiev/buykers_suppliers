"""Admin"""

from django.contrib import admin

from .category import CategoryAdmin
from .product import ProductAdmin

from ..models import (
    Product,
    Category,
    Page
)


admin.site.register(Page)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
