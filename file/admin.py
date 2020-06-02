from django.contrib import admin

# Register your models here.
from django.contrib import admin
from file.models import FileData


class AdminFileData(admin.ModelAdmin):
    pass


admin.site.register(FileData, AdminFileData)
