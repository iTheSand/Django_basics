import json
import os
from datetime import datetime
import random

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'

    products = Product.objects.all()[:4]

    content = {
        'title': title,
        'products': products,
        'basket': get_basket(request.user)
    }

    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category=category_item)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category_item,
            'products': products_list,
            'basket': get_basket(request.user)
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    # same_products = Product.objects.all()[:4]

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product,
        'special_offer': datetime.now(),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    content = {
        'title': 'продукт',
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': ProductCategory.objects.all(),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    title = 'Контакты'
    locations = []
    with open(os.path.join(settings.BASE_DIR, 'contacts.json'), encoding='utf-8') as f:
        locations = json.load(f)

    content = {
        'title': title,
        'locations': locations,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', content)
