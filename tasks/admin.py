from django.contrib import admin

from .models import TaskModel

# Register your models here.


class CustomTaskModelAdmin(admin.ModelAdmin):
    list_display = ("user", "title")


admin.site.register(TaskModel, CustomTaskModelAdmin)
