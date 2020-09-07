from datetime import datetime

from django.test import TestCase

from shop.utils import generate_order_id
from carts.models import Cart, CartItem
from shop.models import Product, Brand, Category


class TestCartModels(TestCase):
    def setUp(self) -> None:
        self.cart = Cart.objects.create(
            customer=None, completed=False
        )
        self.cart.cart_id = generate_order_id(self.cart.id)
        self.cart.save()

        self.cat1 = Category.objects.create(name='Hoodie')
        self.cat2 = Category.objects.create(name='Trousers')

        self.brand1 = Brand.objects.create(name='Crocodile')
        self.brand2 = Brand.objects.create(name='Giorgio')

        self.prod1 = Product.objects.create(
            name='casual hoodie', category=self.cat1, brand=self.brand1, gender='woman',
            age='adult', description='short description', net_price=123.32, vat=.23
        )
        self.prod2 = Product.objects.create(
            name='casual trousers', category=self.cat2, brand=self.brand2, gender='man',
            age='adult', description='short description', net_price=321.32, vat=.23
        )

    def test_cart_is_assigned_cart_id_on_creation(self):
        self.assertEqual(self.cart.cart_id, generate_order_id(self.cart.id))

    def test_cart_items_number_0(self):
        self.assertEqual(self.cart.items_number, 0)

    def test_cart_items_total_0(self):
        self.assertEqual(self.cart.cart_total, 0)

    def test_cart_create_1_cart_item(self):
        self.create_cart_item(self.prod1, 1)
        self.assertEqual(CartItem.objects.all().count(), 1)
        self.assertEqual(self.cart.items_number, 1)

    def test_cart_items_total_1_item(self):
        self.create_cart_item(self.prod1, 1)
        self.assertEqual(float(self.cart.cart_total), float(self.prod1.total_price))

    def test_cart_get_date(self):
        self.assertEqual(self.cart.get_date, datetime.now().strftime('%Y-%m-%d'))

    def test_cart_item_1_item_total(self):
        self.create_cart_item(self.prod1, 1)
        self.assertEqual(
            float(self.cart.cartitem_set.first().item_total),
            float(self.prod1.total_price)
        )

    def create_cart_item(self, item, qty=1):
        CartItem.objects.create(cart=self.cart, product=item, quantity=qty)
