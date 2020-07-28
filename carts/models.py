from django.db import models

from shop.models import *


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.cart_id

    def item_total(self):
        return round(self.quantity * self.product.total_price, 2)


class Cart(models.Model):
    products_price = models.DecimalField(max_digits=200, decimal_places=2, default=0.0)
    delivery_price = models.DecimalField(max_digits=200, decimal_places=2, default=0.0)
    price_total = models.DecimalField(max_digits=200, decimal_places=2, default=0.0)

