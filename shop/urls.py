from django.urls import path

from shop.views import ProductDetail, ProductList, CategoryList, CityList

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<str:name>/', ProductDetail.as_view(), name='product-detail'),
    path('cities/', CityList.as_view(), name='city-list'),
]
