from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic.base import View

from orders.models import Order
from .models import *
from shop.models import Product
from shop.utils import generate_order_id


def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            cart = Cart.objects.get(customer=customer, completed=False)
            items = cart.cartitem_set.all()

        except ObjectDoesNotExist:
            messages.warning(request, "You do not have an active order")
            return redirect('store-main')

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


class CheckoutView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            try:
                cart = Cart.objects.get(customer=customer, completed=False)
                addresses = customer.address_set.all().order_by('-id')
                items = cart.cartitem_set.all()

            except ObjectDoesNotExist:
                messages.warning(self.request, "You do not have an active order")
                return redirect('store-main')
        else:
            return redirect('login')
            # items = []
            # addresses = []
            # cart = {
            #     'items_number': 0,
            #     'cart_total': 0,
            # }
        context = {
            'items': items,
            'cart': cart,
            'addresses': addresses,
        }
        return render(self.request, 'shop/pages/checkout.html', context)

    def post(self, *args, **kwargs):
        data = self.request.POST
        customer = self.request.user.customer
        try:
            cart = Cart.objects.get(customer=customer, completed=False)
            order, created = Order.objects.get_or_create(customer=customer, cart=cart)
            delivery_address = data['address-delivery']
            invoice_address = data['address-invoice']
            # TODO:
            #  Change order id when order is completed not when it's changed
            # order.order_id = generate_order_id(id=order.id)

            order.shipping_address = customer.address_set.get(id=delivery_address)
            order.invoice_address = customer.address_set.get(id=invoice_address)
            order.save()

            return redirect('checkout-confirm')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('store-main')


def add_to_cart(request):
    product_id = request.POST['productId']
    action = request.POST['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
    if created:
        cart.cart_id = generate_order_id(cart.id)
        cart.save()
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
