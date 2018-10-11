from django.contrib import admin


class GoodAdmin(admin.ModelAdmin):
    """Good admin"""

    exclude = ()
