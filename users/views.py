from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CreateUserForm


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        messages.info(request, 'Username or password is incorrect')
    return render(request, 'users/login.html')


# @login_required(login_url='login')
def logoutView(request):
    logout(request)
    return redirect('login')


def registerView(request):
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
