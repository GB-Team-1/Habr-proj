from django.contrib import admin

# Register your models here.
from posts.models import PostCategory, Posts, Links, Comment


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'tags', 'is_published', 'is_active','is_moderated')
    list_filter = ('is_active','is_moderated')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user',  'is_active')
    list_filter = ('is_active',)


