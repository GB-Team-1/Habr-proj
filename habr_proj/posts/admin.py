from django.contrib import admin

# Register your models here.
from posts.models import PostCategory, Posts, Links


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'tags', 'body', 'is_published', 'is_active',)
    list_filter = ('is_active',)


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'link',)
