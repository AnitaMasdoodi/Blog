from django.contrib import admin
from .models import (Category, Post,
                     Comment, Aboutme)


class PostTabularAdmin(admin.TabularInline):
    model = Post
    fields = ('title', 'text', 'author', 'image')
    extra = 0


@admin.register(Category)
class CatgeoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title', )
    inlines = [PostTabularAdmin]


class CommentsInline(admin.StackedInline):
    model = Comment
    fields = ('user', 'text')
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'text']
    list_filter = ['title']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Mark selected comments as approved"

admin.site.register(Comment, CommentAdmin)

admin.site.register(Aboutme)