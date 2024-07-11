from django.contrib import admin

from shop.models import Category, Product, Topping, City, Restaurant, Service, Language

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Topping)
admin.site.register(City)
admin.site.register(Restaurant)
admin.site.register(Service)
admin.site.register(Language)
