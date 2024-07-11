import django_filters

from shop.models import Product, Restaurant, City


class ProductFilter(django_filters.FilterSet):
    SORT_CHOICES = (
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

    class Meta:
        model = Product
        fields = ['category', 'sort_by']

    def filter_sort_by(self, queryset, name, value):
        if value == 'newest':
            return queryset.order_by('-created_at')
        elif value == 'price_asc':
            return queryset.order_by('price')
        elif value == 'price_desc':
            return queryset.order_by('-price')
        elif value == 'alphabetical':
            return queryset.order_by('title')
        else:
            return queryset


class RestaurantFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='city__slug')

    class Meta:
        model = Restaurant
        fields = ['city']
