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


class OrderAddress(models.Model):
    name = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    company_name = models.CharField(max_length=200, blank=True, null=True)
    tax_number = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.name}'
