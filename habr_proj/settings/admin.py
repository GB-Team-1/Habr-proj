from django.contrib import admin

# Register your models here.
from settings.models import Help


@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):
    list_display = ('title',)