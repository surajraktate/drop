from django.contrib import admin

# Register your models here.
from django.contrib import admin
from clipboard.models import ClipBoardData


class AdminClipBoard(admin.ModelAdmin):
    pass


admin.site.register(ClipBoardData, AdminClipBoard)
