from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from users import views as user_views


urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store_main, name='store-main'),
    path('store/<str:gender>/', views.store_detail, name='store'),
    path('store/<str:gender>/<str:category>/', views.store_detail, name='store-category'),
    path('product/<str:pk>/', views.product, name='product-detail'),

    path('cart/', include('carts.urls')),
    path('customer/', include('users.urls')),

    # Staff views
    path('dashboard/', views.dashboard, name='admin-dashboard'),
    path('dashboard/customer/<str:id>/', views.dashboardCustomer, name='admin-dashboard-client'),

]
