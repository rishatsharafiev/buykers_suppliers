from django.contrib import admin


class PictureAdmin(admin.ModelAdmin):
    """Picture admin"""

    exclude = ()
