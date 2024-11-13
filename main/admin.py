from django.contrib import admin
from .models import News



@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'views', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('created_at',)