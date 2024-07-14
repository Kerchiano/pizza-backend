from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, City, Restaurant, Review, Rating, Order, OrderItem
from shop.models import Address

User = get_user_model()


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
        fields = ['id', 'address', 'image', 'phone_number', 'open_time', 'close_time', 'description', 'city',
                  'category',
                  'service', 'slug']


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.SlugRelatedField(queryset=Rating.objects.all(), slug_field='name')
    user = serializers.EmailField(required=False)
    restaurant = serializers.SlugRelatedField(queryset=Restaurant.objects.all(), slug_field='slug')
    first_name = serializers.CharField(max_length=150, required=False)
    phone_number = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = Review
        fields = ["rating", "review", "user", "restaurant", "first_name", "phone_number"]

    def create(self, validated_data):
        email = validated_data.get('user')
        user_data = {
            'email': validated_data.pop('user', None),
            'first_name': validated_data.pop('first_name', None),
            'phone_number': validated_data.pop('phone_number', None)
        }
        user, created = User.objects.get_or_create(email=email, defaults=user_data)
        validated_data['user'] = user

        return super().create(validated_data)


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all()
    )
    city = serializers.CharField(source='get_city_display', read_only=True)

    class Meta:
        model = Address
        fields = ['user', 'city', 'street', 'house_number', 'floor', 'entrance']


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    restaurant = serializers.SlugRelatedField(slug_field='slug', queryset=Restaurant.objects.all(), required=False)
    user = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    phone_number = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = Order
        fields = ['user', 'first_name', 'phone_number', 'total_amount', 'delivery_address', 'restaurant',
                  'payment_method', 'delivery_date',
                  'delivery_time', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        email = validated_data.pop('user')
        user_data = {
            'email': email,
            'first_name': validated_data.pop('first_name', ''),
            'phone_number': validated_data.pop('phone_number', '')
        }

        user, created = User.objects.get_or_create(email=email, defaults=user_data)
        order = Order.objects.create(user=user, **validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
