from django.contrib import admin

from ...models.picture import Picture


class PictureInline(admin.TabularInline):
    """Picture inline"""

    model = Picture
