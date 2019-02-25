"""Admin"""

from django.contrib import admin

from .category import CategoryAdmin
from .category_info import CategoryInfoAdmin
from .page import PageAdmin
from .product import ProductAdmin

from ..models import (
    Product,
    Category,
    CategoryInfo,
    Page
)


admin.site.register(Page, PageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryInfo, CategoryInfoAdmin)

admin.site.site_header = 'Справочник мото продукции'
admin.site.site_title = 'Справочник мото продукции'
admin.site.index_title = 'Панель управления'
