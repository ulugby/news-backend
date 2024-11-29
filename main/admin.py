from django.contrib import admin
from .models import News, Config
from django.contrib import messages


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            obj.send_to_telegram()
            
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'author', 'views', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('created_at',)


class ConfigAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

    def has_add_permission(self, request):
        if Config.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Config, ConfigAdmin)