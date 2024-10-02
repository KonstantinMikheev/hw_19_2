from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'is_published', 'views_count', 'created_at',)
    list_filter =('created_at', 'title', 'is_published',)
    search_fields = ('title', 'body',)