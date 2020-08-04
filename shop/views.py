from django.shortcuts import render
from .models import (
        Product,
    )


# Create your views here.
def home(request):
    return render(request, 'shop/pages/index.html')


def store_main(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop/pages/store.html', context)


def store_man(request):
    products = Product.objects.filter(gender='man')
    context = {
        'products': products,
    }
    return render(request, 'shop/pages/store.html', context)


def store_woman(request):
    products = Product.objects.filter(gender='woman')
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