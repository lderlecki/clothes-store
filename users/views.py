from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from carts.models import Cart
from .forms import (
    CreateUserForm,
    CustomerDataForm,
    SetNewPasswordForm,
    AddressForm,
    )

LOGIN_URL = '/customer/login/'


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        messages.info(request, 'Username or password is incorrect')
    return render(request, 'users/login.html')


def logoutView(request):
    logout(request)
    return redirect('login')


def registerView(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created!')
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


@login_required(login_url='login')
def accountView(request):
    return render(request, 'users/account.html')


@login_required(login_url='login')
def editAccountView(request):
    user = request.user
    password_form = SetNewPasswordForm(user=user)
    customer_form = CustomerDataForm(instance=user.customer)
    if request.method == 'POST':
        data = request.POST
        customer_form = CustomerDataForm(data, instance=user.customer)
        if customer_form.is_valid():
            instance = customer_form.save()
            messages.success(request, 'Your data has been updated')
            if data['password']:
                password_form = SetNewPasswordForm(data, user=user)
                if password_form.is_valid():
                    password_form.save(user)
                    messages.success(request, 'Your password has been changed')

    context = {
        'customer_form': customer_form,
        'password_form': password_form,
    }

    return render(request, 'users/account-edit.html', context)


@login_required(login_url='login')
def orderHistoryView(request):
    customer = request.user.customer
    orders = Cart.objects.all()

    context = {
        'orders': orders,
    }
    return render(request, 'users/account-order-history.html', context)


@login_required(login_url='login')
def addressAccountView(request):
    customer = request.user.customer
    addresses = customer.address_set.all()
    context = {
        'addresses': addresses
    }

    return render(request, 'users/account-address-list.html', context)


def addressAddView(request):
    customer = request.user.customer
    address_form = AddressForm(instance=customer)
    if request.method == 'POST':
        data = request.POST
        address_form = AddressForm(data)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = customer
            # TODO: Check whether the new address is set to default,
            #       if so change the existing default address to False
            address.save()
            messages.success(request, 'You have added a new address')
        return redirect('address-list')

    context = {
        'address_form': address_form,
    }

    return render(request, 'users/add-address.html', context)
