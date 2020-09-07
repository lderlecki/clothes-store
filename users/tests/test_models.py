from django.contrib.auth.models import User
from django.test import TestCase

from carts.models import Cart, CartItem
from shop.models import Product, Brand, Category
from users.models import Customer, Address


class TestUsersModels(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('testuser', password='testing321')
        data = {
            'user': self.user,
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '999888777',
            'email': 'test@test.com',
        }
        self.customer = Customer.objects.create(**data)
        self.cart = Cart.objects.create(
            customer=self.customer, completed=False
        )

        cat1 = Category.objects.create(name='Hoodie')
        cat2 = Category.objects.create(name='Trousers')

        brand1 = Brand.objects.create(name='Crocodile')
        brand2 = Brand.objects.create(name='Giorgio')

        self.prod1 = Product.objects.create(
            name='casual hoodie', category=cat1, brand=brand1, gender='woman',
            age='adult', description='short description', net_price=123.32, vat=.23
        )
        self.prod2 = Product.objects.create(
            name='casual trousers', category=cat2, brand=brand2, gender='man',
            age='adult', description='short description', net_price=321.32, vat=.23
        )

    def test_customer_model_valid_data_and_initial_parameters_values(self):
        data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'phone': '999888777',
            'email': 'test@gmail.com',
        }
        customer = Customer.objects.create(**data)
        self.assertTrue(Customer.objects.filter(
            first_name='John', last_name='Smith', phone=999888777, email='test@gmail.com'
        ).exists())
        self.assertEqual(customer.total_cart_items, 0)
        self.assertEqual(str(customer), 'John Smith')
        self.assertFalse(customer.has_active_cart)

    def test_customer_model_with_active_cart(self):
        self.create_cart_item(self.prod1)
        self.assertEqual(self.customer.total_cart_items, 1)
        self.assertTrue(self.customer.has_active_cart)

    def test_customer_model_with_cart_completed(self):
        self.create_cart_item(self.prod1)
        self.cart.completed = True
        self.cart.save()

        self.assertEqual(self.customer.total_cart_items, 0)
        self.assertFalse(self.customer.has_active_cart)

    def create_cart_item(self, item, qty=1):
        CartItem.objects.create(cart=self.cart, product=item, quantity=qty)

    def test_address_model_valid_data_no_customer(self):
        data = {
            'name': 'AddressName', 'customer': self.customer, 'first_name': 'John',
            'last_name': 'Smith', 'company_name': '', 'tax_number': '', 'street': 'Street',
            'number': '123', 'zip_code': '99-999', 'city': 'Warsaw',
            'country': 'Poland', 'phone': '999-888-777', 'default': True, 'address_type': 'B'
        }
        address = Address.objects.create(**data)
        self.assertTrue(Address.objects.filter(**data).exists())
        self.assertEqual(str(address), 'John Smith AddressName')

    def test_address_model_save_valid_data_change_default_address(self):
        data = {
            'name': 'AddressName', 'customer': self.customer, 'first_name': 'John',
            'last_name': 'Smith', 'company_name': '', 'tax_number': '', 'street': 'Street',
            'number': '123', 'zip_code': '99-999', 'city': 'Warsaw',
            'country': 'Poland', 'phone': '999-888-777', 'default': True, 'address_type': 'B'
        }
        Address.objects.create(**data)
        data['name'] = 'New Default Address'
        address_new = Address.objects.create(**data)

        self.assertTrue(address_new.default)
        self.assertFalse(Address.objects.get(name='AddressName').default)
