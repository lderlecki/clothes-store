from django.db import models

from carts.models import Cart

from users.models import Customer, Address

ORDER_STATUS_CHOICES = (
    ('started', 'Started'),
    ('pending', 'Pending'),
    ('delivered', 'Delivered')
)


class Order(models.Model):
    order_id = models.CharField(max_length=150, default='not_completed')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='started')
    date_ordered = models.DateField(auto_now_add=True, auto_now=False)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True,
                                         related_name='shipping_address')
    invoice_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True,
                                        related_name='invoice_address')

    @property
    def get_date(self):
        return self.date_ordered.strftime('%Y-%m-%d')

    @property
    def get_addresses(self):
        return [self.shipping_address, self.invoice_address]
