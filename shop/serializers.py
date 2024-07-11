from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, City, Restaurant


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category = serializers.StringRelatedField()
    topping = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RestaurantSerializer(ModelSerializer):
    open_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])
    close_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])
    city = serializers.StringRelatedField()
    category = serializers.StringRelatedField(many=True)
    service = serializers.StringRelatedField(many=True)

    class Meta:
        model = Restaurant
        fields = ['address', 'image', 'phone_number', 'open_time', 'close_time', 'description', 'city', 'category',
                  'service', 'slug']
