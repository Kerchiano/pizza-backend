from django.contrib import admin

from shop.models import Category, Product, Topping, City

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Topping)
admin.site.register(City)
