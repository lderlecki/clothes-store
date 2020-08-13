from django.http import JsonResponse, Http404
from django.shortcuts import render
from .models import *
from shop.models import Product

import json


# Create your views here.
def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
        items = cart.cartitem_set.all()
    else:
        items = []
        cart = {
            'items_number': 0,
            'cart_total': 0,
        }

    context = {
        'items': items,
        'cart': cart,
    }

    return render(request, 'shop/pages/cart.html', context)


def checkout_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
        items = cart.cartitem_set.all()
    else:
        items = []
        cart = {
            'items_number': 0,
            'cart_total': 0,
        }

    context = {
        'items': items,
        'cart': cart,
    }
    print(context)
    return render(request, 'shop/pages/checkout.html', context)


def add_to_cart(request):
    product_id = request.POST['productId']
    action = request.POST['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
    cart_product, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if action == 'add':
        cart_product.quantity += 1
    elif action == 'remove':
        cart_product.quantity -= 1

    cart_product.save()
    if cart_product.quantity <= 0:
        cart_product.delete()

    context = {
        'product_qty': cart_product.quantity,
        'product_total': cart_product.item_total,
        'cart_items': cart.items_number
    }
    return JsonResponse(context, safe=False)


def get_cart_data(request):
    if request.is_ajax():
        customer = request.user.customer
        cart = Cart.objects.filter(customer=customer, completed=False)
        if cart.exists():
            cart = cart.first()
            context = {
                'cart_total': cart.cart_total,
                'cart_items': cart.items_number,
            }
            return JsonResponse(context, safe=False)
    return Http404
