from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, City, Restaurant, Review, Rating, Order, OrderItem, Service, Topping
from shop.models import Address

User = get_user_model()


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DateOnlyField(serializers.Field):
    def to_representation(self, value):
        return value if value else None


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['id', 'title', 'price']


class ProductSerializer(ModelSerializer):
    price = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    topping = ToppingSerializer(many=True, read_only=True)
    created_at = DateOnlyField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_price(self, obj):
        if obj.price % 1 == 0:
            return int(obj.price)
        return obj.price


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'icon']


class RestaurantSerializer(ModelSerializer):
    open_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])
    close_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'])
    city = serializers.StringRelatedField()
    service = ServiceSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'address', 'image_thumbnail', 'image_detail', 'phone_number', 'open_time', 'close_time',
                  'description', 'city',
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

    # city = serializers.ChoiceField(choices=Address.CITY_CHOICES, required=True)

    class Meta:
        model = Address
        fields = ['user', 'id', 'city', 'street', 'house_number', 'floor', 'entrance', 'flat']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['city'] = instance.get_city_display()
    #     return representation

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=False,
        allow_null=True
    )
    topping = serializers.PrimaryKeyRelatedField(
        queryset=Topping.objects.all(),
        required=False,
        allow_null=True
    )
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['product', 'topping', 'quantity']

    def validate(self, data):
        if not data.get('product') and not data.get('topping'):
            raise serializers.ValidationError("Either 'product' or 'topping' must be provided.")
        return data


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)

    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        required=False,
        allow_null=True
    )
    delivery_address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
        required=False,
        allow_null=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True
    )

    class Meta:
        model = Order
        fields = [
            'user', 'total_amount', 'paid_amount', 'remaining_amount', 'delivery_address', 'restaurant',
            'payment_method', 'delivery_date', 'delivery_time', 'order_items'
        ]

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')

        # Create the order using the existing user
        order = Order.objects.create(**validated_data)

        # Create OrderItems for each entry in the order_items list
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
