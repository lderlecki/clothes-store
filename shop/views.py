from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'shop/pages/index.html')


def store(request):
    context = {}
    return render(request, 'shop/pages/store.html', context)


def cart(request):
    context = {}
    return render(request, 'shop/pages/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'shop/pages/checkout.html', context)