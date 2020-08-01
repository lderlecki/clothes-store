from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store-main'),
    path('product/<str:pk>/', views.product, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

]
