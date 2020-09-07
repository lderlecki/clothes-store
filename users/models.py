from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def total_cart_items(self):
        if not self.cart_set.filter(completed=False):
            return 0
        return self.cart_set.get(completed=False).items_number

    @property
    def has_active_cart(self):
        if self.cart_set.filter(completed=False):
            return True
        return False


class Address(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default='My address')
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES, default='S')
    default = models.BooleanField(default=False)

    company_name = models.CharField(max_length=200, blank=True, null=True)
    tax_number = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.name}'

    def save(self, *args, **kwargs):
        if self.default:
            Address.objects.filter(
                customer=self.customer, default=True, address_type=self.address_type
            ).update(default=False)
        super(Address, self).save(*args, **kwargs)

