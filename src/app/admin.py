from django.contrib import admin
from django.contrib.auth.models import User

from app.models import Post, Rubric


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['slug', 'title', 'body', 'rubric', 'status']
    list_display = ['title', 'author', 'rubric', 'published']
    list_display_links = ['title']
    list_filter = ['published', 'status']
    search_fields = ['title', 'author__username']

admin.site.register(Rubric)
