from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView

from shop.filters import ProductFilter, RestaurantFilter
from shop.models import Category, Product, City, Restaurant, Review
from shop.serializers import CategorySerializer, ProductSerializer, CitySerializer, RestaurantSerializer, \
    ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProductDetail(RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        name = self.kwargs['name'].capitalize()
        return get_object_or_404(Product, title=name)


class CityList(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class RestaurantList(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantFilter


class RestaurantDetail(RetrieveAPIView):
    serializer_class = RestaurantSerializer

    def get_object(self):
        slug = self.kwargs['slug']
        return get_object_or_404(Restaurant, slug=slug)


class ReviewCreate(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
