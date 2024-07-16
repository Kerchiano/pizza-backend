import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza_backend.settings')
django.setup()

from shop.models import *

cities = "https://raw.githubusercontent.com/Kerchiano/storage-photos/main/data/cities.json"
services = "https://raw.githubusercontent.com/Kerchiano/storage-photos/main/data/services.json"
topping = "https://raw.githubusercontent.com/Kerchiano/storage-photos/main/data/topping.json"
categories = "https://raw.githubusercontent.com/Kerchiano/storage-photos/main/data/categories.json"
products = "https://raw.githubusercontent.com/Kerchiano/storage-photos/main/data/products.json"
restaurants = "https://raw.githubusercontent.com/Kerchiano/storage-photos/main/data/restaurants.json"
rating = "https://raw.githubusercontent.com/Kerchiano/storage-photos/main/data/rating.json"


def load_json_from_url(url):
    response = requests.get(url)
    data = response.json()
    return data


def create_objects(data, model):
    for item in data:
        model.objects.create(**item)


create_objects(load_json_from_url(cities), City)
create_objects(load_json_from_url(services), Service)
create_objects(load_json_from_url(rating), Rating)
create_objects(load_json_from_url(topping), Topping)
create_objects(load_json_from_url(categories), Category)

instance_category = {category.title: category for category in Category.objects.all()}
instance_toppings = {topping.title: topping for topping in Topping.objects.all()}

for product in load_json_from_url(products):
    category_name = product.pop('category')
    toppings_titles = product.pop('topping', [])

    category = Category.objects.get(title=category_name)
    created_product = Product.objects.create(category=category, **product)

    toppings = [Topping.objects.get(title=topping).id for topping in toppings_titles]
    created_product.topping.set(toppings)

instance_city = {city.name: city for city in City.objects.all()}
instance_service = list(Service.objects.all())

for restaurant in load_json_from_url(restaurants):
    city_name = restaurant.pop('city')
    service_titles = restaurant.pop('service', [])

    city = City.objects.get(name=city_name)
    created_restaurant = Restaurant.objects.create(city=city, **restaurant)

    services = [Service.objects.get(title=service.get('title')).id for service in service_titles]

    created_restaurant.service.set(services)
