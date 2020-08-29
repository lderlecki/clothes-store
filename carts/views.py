import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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
            messages.warning(request, "Yor cart is empty")
            return redirect('store-main')
    else:
        try:
            cart_cookie = json.loads(request.COOKIES['cart'])
        except:
            cart_cookie = {}

        items = []
        cart = {
            'items_number': 0,
            'cart_total': 0,
            'completed': False
        }

        for i in cart_cookie:
            qty = cart_cookie[i]['quantity']
            product = Product.objects.get(id=i)
            item_total = product.total_price * qty

            cart['items_number'] += qty
            cart['cart_total'] += item_total

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'total_price': product.total_price,
                    'image_preview': product.image_preview,
                },
                'quantity': qty,
                'item_total': item_total,
            }
            items.append(item)
    context = {
        'items': items,
        'cart': cart,
    }

    return render(request, 'shop/pages/cart.html', context)


def add_to_cart(request):
    product_id = request.POST['productId']

    if request.user.is_authenticated:
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
        elif action == 'delete':
            cart_product.quantity = 0

        cart_product.save()
        if cart_product.quantity <= 0:
            cart_product.delete()
        context = {
            'product_qty': cart_product.quantity,
            'product_total': cart_product.item_total,
            'cart_items': cart.items_number
        }

    else:
        try:
            cart_cookie = json.loads(request.COOKIES['cart'])
        except:
            cart_cookie = {}
        if len(cart_cookie) > 0:

            pass
        else:
            product_qty = 0
            product_total = 0
            cart_items = 0
        context = {
            'product_qty': product_qty,
            'product_total': product_total,
            'cart_items': cart_items
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


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            try:
                cart = Cart.objects.get(customer=customer, completed=False)
                if cart.items_number <= 0:
                    messages.warning(self.request, "Your cart is empty. Please add products to checkout")
                    return redirect('cart')
                addresses = customer.address_set.all().order_by('-id')
                items = cart.cartitem_set.all()

            except ObjectDoesNotExist:
                messages.warning(self.request, "You do not have any items in cart")
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
        cart = Cart.objects.get(customer=customer, completed=False)
        try:
            if cart.items_number > 0:
                order, created = Order.objects.get_or_create(customer=customer, cart=cart)
                delivery_address = data['address-delivery']
                invoice_address = data['address-invoice']

                if created:
                    order.order_id = generate_order_id(id=order.id)

                order.shipping_address = customer.address_set.get(id=delivery_address)
                order.invoice_address = customer.address_set.get(id=invoice_address)
                order.save()
                self.request.session['order_id'] = order.order_id

                # cart.completed = True
                # cart.save()

                return redirect('checkout-confirm')
            else:
                messages.warning(self.request, "Your cart is empty. Add some products then proceed to checkout")
                return redirect('store-main')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('store-main')


class CheckoutCompleted(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            print(self.request.session['order_id'])
            order = Order.objects.get(order_id=self.request.session['order_id'])
            items = order.cart.cartitem_set.all()

            context = {
                'order': order,
                'items': items,
            }
            return render(self.request, 'shop/pages/order-completed.html', context)

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('store-main')
