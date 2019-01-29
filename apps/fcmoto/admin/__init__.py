"""Admin"""

from django.contrib import admin

from .category import CategoryAdmin
from .page import PageAdmin
from .product import ProductAdmin

from ..models import (
    Product,
    Category,
    Page
)


admin.site.register(Page, PageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
