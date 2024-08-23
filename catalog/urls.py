from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='products'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('contacts/', contacts, name='contacts')
]
