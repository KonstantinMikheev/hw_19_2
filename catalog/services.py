from django.conf import settings
from django.core.cache import cache

from catalog.models import Category, Product


def get_categories_from_cache():
    """
    Get categories from cache. If cache is disabled, retrieve from database.
    Returns:
        QuerySet: All categories from the database or from cache.
    """
    if not settings.CACHE_ENABLED:
        categories = Category.objects.all()
    else:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = Category.objects.all()
            cache.set(key, categories)

    return categories


def get_products_from_cache():
    """
    Get products from cache. If cache is disabled, retrieve from database.
    Returns:
        QuerySet: All products from the database or from cache.
    """

    if not settings.CACHE_ENABLED:
        products = Product.objects.all()
    else:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.all()
            cache.set(key, products)

    return products
