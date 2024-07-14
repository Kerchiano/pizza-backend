from django.contrib import admin

from shop.models import Category, Product, Topping, City, Restaurant, Service, Language, Review, Rating, Address, Order, \
    OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Topping)
admin.site.register(City)
admin.site.register(Restaurant)
admin.site.register(Service)
admin.site.register(Language)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
