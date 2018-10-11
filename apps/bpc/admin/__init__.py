"""Admin"""

from django.contrib import admin

from .good import GoodAdmin
from .picture import PictureAdmin
from .task import TaskAdmin

from ..models import (
    Good,
    Picture,
    Task
)


admin.site.register(Good, GoodAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Task, TaskAdmin)
