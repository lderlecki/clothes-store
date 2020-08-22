from django.shortcuts import render
from .models import (
        Product,
        Category
    )


def home(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'shop/pages/index.html', context)


def store_main(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop/pages/store.html', context)


def store_detail(request, gender, category=None):
    if category:
        products = Product.objects.filter(gender=gender, category__name=category)
    else:
        products = Product.objects.filter(gender=gender)

    context = {
        'products': products,
    }
    return render(request, 'shop/pages/store.html', context)


def product(request, pk):
    item = Product.objects.get(id=pk)
    images = item.product_images.all()
    context = {
        'item': item,
        'images': images,
    }
    return render(request, 'shop/pages/product.html', context)


def cart(request):
    context = {}
    return render(request, 'shop/pages/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'shop/pages/checkout.html', context)
