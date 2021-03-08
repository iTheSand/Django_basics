import json
import os
from datetime import datetime

from django.conf import settings
from django.shortcuts import render

from mainapp.models import Product, ProductCategory


# Create your views here.
def main(request):
    title = 'Главная'
    products = Product.objects.all()[:4]

    content = {
        'title': title,
        'products': products
    }

    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'Продукты'
    same_products = Product.objects.all()[:4]
    links_menu = ProductCategory.objects.all()

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'special_offer': datetime.now()
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    title = 'Контакты'
    locations = []
    with open(os.path.join(settings.BASE_DIR, 'contacts.json'), encoding='utf-8') as f:
        locations = json.load(f)

    content = {
        'title': title,
        'locations': locations
    }
    return render(request, 'mainapp/contact.html', content)
