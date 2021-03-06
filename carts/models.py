from datetime import datetime

from django.db import models

from shop.models import Product
from users.models import Customer

from shop.utils import generate_order_id


COMPLETED_CHOICES = (
    (True, 'Yes'),
    (False, 'No'),
)


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.cart.cart_id

    @property
    def item_total(self):
        return round(self.quantity * self.product.total_price, 2)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(choices=COMPLETED_CHOICES, default=False)
    cart_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.cart_id}'

    @property
    def items_number(self):
        items = self.cartitem_set.all()
        total = sum([item.quantity for item in items])
        return total

    @property
    def cart_total(self):
        items = self.cartitem_set.all()
        total = sum([item.item_total for item in items])
        return total

    @property
    def get_date(self):
        return self.date_ordered.strftime('%Y-%m-%d')
