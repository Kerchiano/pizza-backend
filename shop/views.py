import django_filters
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView

from shop.filters import ProductFilter
from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer
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
