from django.contrib import admin
from .models import Profile
from home.models import Post

# class PostTabularAdmin(admin.TabularInline):
#     model = Post
#     fields = ('title', 'text', 'author', 'image')
#     extra = 0
 
# @admin.register(Post)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('title', 'date')
#     inlines = [PostTabularAdmin]

admin.site.register(Profile)
