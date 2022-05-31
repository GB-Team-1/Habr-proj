from django.contrib import admin

from authapp.models import HabrUser


@admin.register(HabrUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', )
    list_filter = ('is_staff',)
    search_fields = ['username',]
