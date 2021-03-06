from django.shortcuts import render, redirect

from orders.models import Order
from users.models import Customer
from .models import Product


def home(request):
    return render(request, 'shop/pages/index.html')


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


def dashboard(request):
    if request.user.is_staff:
        customers = Customer.objects.all()
        orders = Order.objects.all()
        delivered = orders.filter(status='delivered').count()
        pending = orders.filter(status='pending').count()
        started = orders.filter(status='started').count()
    else:
        return redirect('home')

    context = {
        'customers': customers,
        'orders': orders,
        'delivered': delivered,
        'pending': pending,
        'started': started,
        'orders_total': orders.count(),
    }
    return render(request, 'shop/pages/admin-dashboard.html', context)


def dashboardCustomer(request, customer_id):
    if request.user.is_staff:
        customer = Customer.objects.get(id=customer_id)
        orders = customer.order_set.all()
    else:
        return redirect('home')

    context = {
        'customer': customer,
        'orders': orders,
    }

    return render(request, 'shop/pages/dashboard-customer.html', context)
