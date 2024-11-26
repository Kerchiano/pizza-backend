from django.contrib import admin

from shop.models import Category, Product, Topping, City, Restaurant, Service, Review, Rating, Address, Order, \
    OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('remaining_amount',)
        return ()


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Topping)
admin.site.register(City)
admin.site.register(Restaurant)
admin.site.register(Service)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Address)
admin.site.register(OrderItem)
