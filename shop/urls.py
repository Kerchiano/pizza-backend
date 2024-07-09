from django.urls import path

from shop import views

urlpatterns = [
    path('category/', views.CategoryList.as_view(), name='category-list'),
]
