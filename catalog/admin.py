from django.contrib import admin

from catalog.models import Category, Product, ContactData, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'category',)
    list_filter =('category',)
    search_fields = ('title', 'description',)


@admin.register(ContactData)
class ContactDataAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone',)
    list_filter =('name',)
    search_fields = ('name',)

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_name', 'version_flag',)
    list_filter = ('product', 'version_flag',)