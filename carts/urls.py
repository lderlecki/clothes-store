from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    # path('checkout/confirm/<str:id>/', views.checkout_confirm, name='checkout-confirm'),
    path('add_to_cart/', views.add_to_cart, name='add-item'),
    path('get_cart_data/', views.get_cart_data, name='cart-data'),

]
