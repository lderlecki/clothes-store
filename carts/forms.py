from django.forms import ModelForm

from orders.models import OrderAddress
from users.models import Address


class ShippingAddressForm(ModelForm):
    class Meta:
        model = OrderAddress
        fields = ('first_name', 'last_name', 'company_name', 'tax_number',
                  'street', 'number', 'zip_code', 'city', 'country', 'phone')
