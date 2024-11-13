from django.urls import path

from shop.views import ProductDetail, ProductList, CategoryList, CityList, RestaurantList, RestaurantDetail, \
    ReviewCreate, AddressList, AddressDelete, AddressCreate, OrderListCreate

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),

    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetail.as_view(), name='product-detail'),

    path('cities/', CityList.as_view(), name='city-list'),

    path('restaurants/', RestaurantList.as_view(), name='restaurant-list'),
    path('restaurants/<slug:slug>/', RestaurantDetail.as_view(), name='restaurant-detail'),

    path('reviews/', ReviewCreate.as_view(), name='review-create'),

    path('address/', AddressList.as_view(), name='address-list'),
    path('address/create/', AddressCreate.as_view(), name='address-create'),
    path('address/delete/<int:pk>/', AddressDelete.as_view(), name='address-detail'),

    path('orders/', OrderListCreate.as_view(), name='order-list-create'),
]
