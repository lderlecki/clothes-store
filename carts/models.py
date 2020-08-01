from django.db import models

from shop.models import *
from users.models import *


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    def item_total(self):
        return round(self.quantity * self.product.total_price, 2)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    products_price = models.DecimalField(max_digits=200, decimal_places=2, default=0.0)
    delivery_price = models.DecimalField(max_digits=200, decimal_places=2, default=0.0)
    price_total = models.DecimalField(max_digits=200, decimal_places=2, default=0.0)
    cart_id = models.CharField(max_length=200, null=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, blank=True, null=True, on_delete=models.SET_NULL)
    adress = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adress