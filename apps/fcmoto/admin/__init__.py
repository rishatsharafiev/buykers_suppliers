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

admin.site.site_header = 'Справочник мото продукции'
admin.site.site_title = 'Справочник мото продукции'
admin.site.index_title = 'Панель управления'
