from django.contrib import admin

# Register your models here.
from posts.models import PostCategory


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
