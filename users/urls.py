from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('register/', views.registerView, name='register'),

    path('account/', views.accountView, name='account'),
    path('account/edit/profile/', views.editAccountView, name='account-edit'),
    path('account/order/history/', views.orderHistoryView, name='order-history'),
    path('account/edit/address/', views.addressAccountView, name='account-address'),
]
