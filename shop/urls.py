from django.urls import path

from shop import views
from shop.views import ProductDetail, ProductList, CategoryList

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<str:name>/', ProductDetail.as_view(), name='product-detail'),
]
