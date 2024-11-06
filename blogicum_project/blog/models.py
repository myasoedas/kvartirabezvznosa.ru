# blogicum/blog/models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator

from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.timezone import now

from .constants import CHAR_FIELD_MAX_LENGTH, SELF_TEXT_MAX_LENGTH

User = get_user_model()


class PublishableModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class TitleModel(models.Model):
    title = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH,
        verbose_name='Заголовок'
    )

    class Meta:
        abstract = True


class Location(PublishableModel):
    name = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ['name']

    def __str__(self):
        return Truncator(self.name).chars(
            SELF_TEXT_MAX_LENGTH, truncate='...')


class Category(PublishableModel, TitleModel):
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы,'
            ' цифры, дефис и подчёркивание.',
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return Truncator(self.title).chars(
            SELF_TEXT_MAX_LENGTH, truncate='...')


class Post(PublishableModel, TitleModel):
    text = CKEditor5Field(config_name='default', verbose_name="Текст публикации")

    image = models.ImageField(
        upload_to='blogs_images/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )

    pub_date = models.DateTimeField(
        default=now,  # Устанавливает текущее время по умолчанию
        verbose_name='Дата и время публикации',
        help_text=_(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        ),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )

    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.id})

    def __str__(self):
        return self.title


class Comment(PublishableModel, models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',  # Добавляем related_name
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к посту {self.post}'
