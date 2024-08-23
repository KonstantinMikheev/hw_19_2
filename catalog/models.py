from django.db import models


NULLABLE = {"blank": True, "null": True}  # Делает поле необязательным к заполнению


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание категории", **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("title",)


class Product(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание продукта", **NULLABLE
    )
    preview = models.ImageField(
        upload_to="products/image", verbose_name="Изображение", **NULLABLE
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", **NULLABLE
    )
    price = models.IntegerField(verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = (
            "title",
            "category",
            "price",
        )

class ContactData(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    message = models.TextField(verbose_name="Запрос пользователя", help_text="Введите Ваш запрос.", **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания (записи в БД)')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ('name',)

    def __str__(self):
        return f"Contact: {self.name}, {self.phone}"

