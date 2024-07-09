from django.db import models

from pizza_backend import settings

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    title = models.CharField(max_length=100)
    icon = models.URLField(max_length=500)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    topping = models.ManyToManyField('Topping')

    def __str__(self):
        return self.title


class Topping(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.title
