from django.db import models

from users.models import User

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

    owner = models.ForeignKey(
        User,
        verbose_name="владелец",
        help_text='Укажите производителя',
        on_delete=models.SET_NULL,
        **NULLABLE
        )

    is_published = models.BooleanField(verbose_name="Опубликовано ", default=False)

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
        permissions = [
            ('change_is_published', 'User can change the status of product'),
            ('change_description', 'User can change the description of product'),
            ('change_category', 'User can change the category of product'),
        ]


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


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="versions", verbose_name="продукт")
    version_number = models.PositiveIntegerField(default=0, verbose_name="номер версии")
    version_name = models.CharField(max_length=150, verbose_name="название версии")
    version_flag = models.BooleanField(default=True, verbose_name="актуальная версия")

    def __str__(self):
        return f"{self.product} {self.version_number} {self.version_name} {self.version_flag}"

    class Meta:
        verbose_name = "версия продукта"
        verbose_name_plural = "версии продуктов"
        constraints = [
            models.UniqueConstraint(fields=['product', 'version_number'], name='unique_product_version')
        ]
