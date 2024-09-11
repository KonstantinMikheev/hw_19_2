from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactsDataView, ProductCreateView, ProductUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    # path('', home, name='products'),
    path('', ProductListView.as_view(), name='product_list'),
    # path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('contacts/', ContactsDataView.as_view(), name='contacts'),
    # path('contacts/', contacts, name='contacts'),
]
