from rest_framework.generics import ListAPIView

from shop.models import Category
from shop.serializers import CategorySerializer


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

