from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from users import views as user_views


urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store_main, name='store-main'),
    path('store/man/', views.store_man, name='store-man'),
    path('store/woman/', views.store_woman, name='store-woman'),
    path('product/<str:pk>/', views.product, name='product-detail'),
    path('cart/', include('carts.urls')),
    path('customer/', include('users.urls')),

]
