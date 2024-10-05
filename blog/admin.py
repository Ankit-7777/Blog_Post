from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'published_date')
    list_filter = ('created_date', 'published_date', 'author')
    search_fields = ('title', 'content', 'tags__name')

    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'content', 'tags')
        }),
        ('Media', {
            'fields': ('image', 'video'),
            'classes': ('collapse',)
        }),
        ('Author and Dates', {
            'fields': ('author', 'created_date', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_date', 'published_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date', 'approved')
    list_filter = ('approved', 'created_date', 'post', 'author')
    search_fields = ('text', 'author__username')

    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'author', 'text')
        }),
        ('Status and Actions', {
            'fields': ('approved', 'likes'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_date',)
