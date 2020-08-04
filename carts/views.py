from django.shortcuts import render
from .models import *


# Create your views here.
def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
        items = cart.cartitem_set.all()
    else:
        items = []

    context = {
        'items': items,
        'cart': cart,
    }

    return render(request, 'shop/pages/cart.html', context)
