import django_filters

from shop.models import Product, Restaurant, Address, Order


class ProductFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ('popular', 'Popular'),
        ('newest', 'Newest'),
        ('price_asc', 'Price Ascending'),
        ('price_desc', 'Price Descending'),
        ('alphabetical', 'Alphabetical'),
    )

    sort_by = django_filters.ChoiceFilter(
        choices=SORT_CHOICES,
        method='filter_sort_by',
        label='Sort By'
    )

    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category', 'sort_by']

    def filter_sort_by(self, queryset, name, value):
        if value == 'popular':
            return queryset
        elif value == 'newest':
            return queryset.order_by('-id')
        elif value == 'price_asc':
            return queryset.order_by('price')
        elif value == 'price_desc':
            return queryset.order_by('-price')
        elif value == 'alphabetical':
            return queryset.order_by('title')
        else:
            return queryset


class RestaurantFilter(django_filters.FilterSet):
    city_slug = django_filters.CharFilter(field_name='city__slug')

    class Meta:
        model = Restaurant
        fields = ['city_slug']


class AddressFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name='user_id')

    class Meta:
        model = Address
        fields = ['user']


class UserOrderFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Order
        fields = ['user']
