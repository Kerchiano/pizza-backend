from django.db import models
from django.utils import timezone

from pizza_backend import settings
from shop.mixins import SlugMixin

User = settings.AUTH_USER_MODEL


class Category(SlugMixin):
    title = models.CharField(max_length=100)
    icon = models.URLField(max_length=500)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Product(SlugMixin):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.URLField(max_length=500)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    topping = models.ManyToManyField('Topping', related_name='products')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Topping(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.title


class City(SlugMixin):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=100)
    icon = models.URLField(max_length=500)

    def __str__(self):
        return self.title


class Restaurant(SlugMixin):
    address = models.CharField(max_length=255, unique=True)
    image_thumbnail = models.URLField(max_length=500)
    image_detail = models.URLField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(unique=True, max_length=40)
    open_time = models.TimeField()
    close_time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)

    def __str__(self):
        return self.address


class Rating(models.Model):
    name = models.CharField(max_length=100)
    icon = models.URLField(max_length=500)

    def __str__(self):
        return self.name


class Review(models.Model):
    review = models.TextField()
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    CITY_CHOICES = [
        ('K', 'Київ'),
        ('Kh', 'Харків'),
        ('D', 'Дніпро'),
        ('M', 'Миколаїв'),
    ]
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='K')
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)
    floor = models.CharField(max_length=10, blank=True, null=True)
    entrance = models.CharField(max_length=10, blank=True, null=True)
    flat = models.CharField(max_length=50, blank=True, null=True)


class Meta:
    verbose_name_plural = "Addresses"


def __str__(self):
    return f"{self.street}, {self.house_number}, {self.floor or ''}, {self.entrance or ''}"


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('G', 'Готівкою'),
        ('C', 'Картою'),
        ('Q', 'QR-код')
    ]

    DELIVERY_TIME_CHOICES = [(f"{hour:02}:{minute:02}", f"{hour:02}:{minute:02}")
                             for hour in range(12, 23)
                             for minute in [0, 15, 30, 45]]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    paid_amount = models.IntegerField(blank=True, null=True, default=0)
    remaining_amount = models.IntegerField(blank=True, null=True, editable=False, default=0)
    created_at = models.DateField(auto_now_add=True)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, blank=True, null=True)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES, default='Г')
    delivery_date = models.DateField(default=timezone.now)
    delivery_time = models.CharField(max_length=5, choices=DELIVERY_TIME_CHOICES, default='12:00')

    def save(self, *args, **kwargs):
        if self.total_amount is not None and self.paid_amount is not None and self.paid_amount != 0:
            self.remaining_amount = self.paid_amount - self.total_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    topping = models.ForeignKey('Topping', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order.id)
