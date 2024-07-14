from django.db import models

from pizza_backend import settings
from shop.mixins import SlugMixin

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    title = models.CharField(max_length=100)
    icon = models.URLField(max_length=500)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Product(SlugMixin):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    topping = models.ManyToManyField('Topping')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


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


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Restaurant(SlugMixin):
    address = models.CharField(max_length=255, unique=True)
    image = models.URLField(max_length=500)
    phone_number = models.CharField(unique=True, max_length=10)
    open_time = models.TimeField()
    close_time = models.TimeField()
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
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
    GENDER_CHOICES = [
        ('K', 'Київ'),
        ('Kh', 'Харків'),
        ('D', 'Дніпро'),
        ('M', 'Миколаїв'),
    ]
    city = models.CharField(max_length=2, choices=GENDER_CHOICES, default='K')
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)
    floor = models.CharField(max_length=10, blank=True, null=True)
    entrance = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street}, {self.house_number}, {self.floor or ''}, {self.entrance or ''}"
