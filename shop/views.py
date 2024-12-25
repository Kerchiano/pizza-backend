from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, \
    DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.filters import ProductFilter, RestaurantFilter, AddressFilter, UserOrderFilter
from shop.models import Category, Product, City, Restaurant, Review, Order
from shop.permissions import IsOwnerOrAdmin
from shop.serializers import CategorySerializer, ProductSerializer, CitySerializer, RestaurantSerializer, \
    ReviewSerializer, AddressSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend

from shop.models import Address


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
        slug = self.kwargs['slug']
        return get_object_or_404(Product, slug=slug)


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


class AddressList(ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AddressFilter

    def list(self, request, *args, **kwargs):
        if 'user' not in request.query_params:
            return Response({"detail": "The 'user' parameter is required."}, status=400)

        return super().list(request, *args, **kwargs)


class AddressDelete(DestroyAPIView):
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Address, pk=pk)


class AddressCreate(CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class OrderListCreate(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserOrderFilter
