from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactsDataView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    # path('', home, name='products'),
    path('', ProductListView.as_view(), name='product_list'),
    # path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('contacts/', ContactsDataView.as_view(), name='contacts'),
    # path('contacts/', contacts, name='contacts'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
]
