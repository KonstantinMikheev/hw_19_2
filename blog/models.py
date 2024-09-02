from django.db import models

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


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)  # Сортировка по дате создания в обратном порядке

