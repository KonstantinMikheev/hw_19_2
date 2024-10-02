import json
from gettext import Catalog

from django.core.management import BaseCommand

from catalog.admin import CategoryAdmin
from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('categories.json', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def json_read_products():
        with open('products.json', encoding='utf-8') as file:
            return json.load(file)

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(
                Category(
                    pk=category.get('pk'),
                    title=category['fields'].get('title'),
                    description=category['fields'].get('description')
                )
            )
        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(
                Product(
                    pk=product.get('pk'),
                    title=product['fields'].get('title'),
                    description=product['fields'].get('description'),
                    preview=product['fields'].get('preview'),
                    category=Category.objects.get(pk=product['fields'].get('category')),
                    price=product['fields'].get('price'),
                    created_at=product['fields'].get('created_at'),
                    updated_at=product['fields'].get('updated_at')
                )
            )
        Product.objects.bulk_create(product_for_create)
