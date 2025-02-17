from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *  # Импортируйте модели, которые хотите зарегистрировать


# Регистрация модели Posts с собственным классом администратора
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'category', 'content', 'likes', 'photo', 'get_html_photo', 'is_published', 'time_create',
              'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        return ""  # Добавьте этот возврат на случай, если photo равно None

    get_html_photo.short_description = 'Photo'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


# Регистрируем Posts модели с использованием класса BlogAdmin
admin.site.register(Posts, BlogAdmin)
admin.site.register(Category, CategoryAdmin)

# Настройки заголовка админки
admin.site.site_title = 'Админка'
admin.site.site_header = 'Комната админа'
