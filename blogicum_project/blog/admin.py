from django.contrib import admin
from django.db import models

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Category, Comment, Location, Post


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = ('title', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)
    empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (CommentInline,)
    list_display = (
        'title',
        'author',
        'category',
        'is_published',
        'pub_date',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'text',)
    list_filter = ('is_published', 'category', 'author', 'pub_date', 'location',)
    list_display_links = ('title',)
    empty_value_display = 'Не задано'

    # Настройка отображения редактора
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }

    # Группировка полей в админке
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'author', 'category', 'location',),
        }),
        ('Изображение', {
            'fields': ('image',),
            'description': 'Добавьте изображение для карточки поста',
        }),
        ('Публикация', {
            'fields': ('is_published', 'pub_date'),
        }),
        ('Дополнительно', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # Только для чтения
    readonly_fields = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created_at', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('author__username', 'text', 'post__title')
    list_filter = ('is_published', 'author', 'post')
    empty_value_display = 'Не задано'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)
    empty_value_display = 'Не задано'


admin.site.empty_value_display = 'Не задано'
