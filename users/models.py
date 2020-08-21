from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def total_cart_items(self):
        if not self.cart_set.get(completed=False):
            return 0
        return self.cart_set.get(completed=False).items_number


class Address(models.Model):
    name = models.CharField(max_length=100, default='Default')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100, default='Default')
    last_name = models.CharField(max_length=100, default='Default')
    phone = models.CharField(max_length=100)

    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    company_name = models.CharField(max_length=200, blank=True, null=True)
    tax_number = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.name}'

    @property
    def get_default(self):
        return self.customer.address_set.filter(default=True)
