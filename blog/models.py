from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}  # Делает поле необязательным к заполнению


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True,
                            blank=True)  # Человекочитаемый адрес, человекочитаемый url
    body = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/images', verbose_name='Изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    author = models.ForeignKey(
        User,
        verbose_name="автор",
        help_text='Укажите автора',
        on_delete=models.SET_NULL,
        **NULLABLE
    )


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)  # Сортировка по дате создания в обратном порядке
        permissions = [
            ('can_edit_is_published', 'Can edit is published'),
            ('can_edit_body', 'Can edit body'),
            ('can_edit_title', 'Can edit title'),
            ('can_edit_preview', 'Can edit preview'),
        ]

