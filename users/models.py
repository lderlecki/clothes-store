from django.contrib.auth.models import User
from django.db import models

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


# class Address(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     street_address = models.CharField(max_length=100)
#     apartment_address = models.CharField(max_length=100)
#     zip = models.CharField(max_length=10)
#     address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
#     default = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.username
