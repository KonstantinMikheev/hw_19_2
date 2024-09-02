from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactsDataView

app_name = CatalogConfig.name

urlpatterns = [
    # path('', home, name='products'),
    path('', ProductListView.as_view(), name='product_list'),
    # path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsDataView.as_view(), name='contacts'),
    # path('contacts/', contacts, name='contacts'),
]
