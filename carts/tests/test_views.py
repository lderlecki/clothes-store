from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from carts.models import Cart, CartItem
from carts.views import cart_view, get_cart_data, add_to_cart

from shop.models import Product, Brand, Category

from users.models import Customer

CART_URL = reverse('cart')
MAIN_URL = reverse('store-main')
ADD_TO_CART = reverse('add-item')
GET_CART_DATA = reverse('cart-data')


class TestCartViewsUnauthenticatedUser(TestCase):
    def setUp(self):
        self.client = Client()
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

    def test_empty_cart_view(self):
        response = self.client.get(CART_URL)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, MAIN_URL)
        self.assertEqual(self.client.session.get('cart_id', None), None)

    def test_add_item_to_cart(self):
        response = self.manage_cart_items(self.prod1, 'add')
        cart = self.get_session_cart()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.client.session.get('cart_id', None), None)
        self.assertEqual(self.client.session.get('cart_id', None), cart.cart_id)
        self.assertEqual(self.client.session.get('total_cart_items'), 1)

    def test_json_response_after_add_item(self):
        response = self.manage_cart_items(self.prod2, 'add')
        content = {
            'product_qty': 1,
            'product_total': str(self.prod2.total_price),
            'cart_items': 1,
        }

        self.assertJSONEqual(str(response.content, encoding='utf8'), content)

    def test_remove_item_from_cart(self):
        _ = self.manage_cart_items(self.prod1, 'add')
        response = self.manage_cart_items(self.prod1, 'remove')
        cart = self.get_session_cart()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.items_number, 0)
        self.assertEqual(self.client.session.get('total_cart_items'), 0)

    def test_json_response_after_remove_item(self):
        _ = self.manage_cart_items(self.prod2, 'add')
        response = self.manage_cart_items(self.prod2, 'remove')
        content = {
            'product_qty': 0,
            'product_total': '0.00',
            'cart_items': 0,
        }

        self.assertJSONEqual(str(response.content, encoding='utf8'), content)

    def test_delete_item_from_cart(self):
        _ = self.manage_cart_items(self.prod1, 'add')
        _ = self.manage_cart_items(self.prod2, 'add')
        response = self.manage_cart_items(self.prod1, 'delete')
        cart = self.get_session_cart()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.items_number, 1)
        self.assertEqual(float(cart.cart_total), self.prod2.total_price)
        self.assertEqual(self.client.session.get('total_cart_items'), 1)

    def test_json_response_after_delete_item(self):
        _ = self.manage_cart_items(self.prod1, 'add')
        _ = self.manage_cart_items(self.prod2, 'add')
        response = self.manage_cart_items(self.prod2, 'delete')
        content = {
            'product_qty': 0,
            'product_total': '0.00',
            'cart_items': 1,
        }

        self.assertJSONEqual(str(response.content, encoding='utf8'), content)

    def test_get_cart_data_empty_cart(self):
        response = self.client.get(GET_CART_DATA)
        self.assertEqual(response.status_code, 404)

    def test_cart_data_1_item(self):
        _ = self.manage_cart_items(self.prod1, 'add')
        response = self.client.get(GET_CART_DATA, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        content = {
            'cart_total': str(self.prod1.total_price),
            'cart_items': 1,
        }

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), content)

    def manage_cart_items(self, product, action):
        data = {
            'productId': product.id,
            'action': action
        }
        return self.client.post(ADD_TO_CART, data)

    def get_session_cart(self):
        return Cart.objects.get(cart_id=self.client.session.get('cart_id'))


class TestCartViewsAuthenticatedUser(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('somelogin', password='testing321')
        Customer.objects.create(user=self.user)

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

    def test_empty_cart_view(self):
        request = self.create_request('POST', CART_URL)
        response = cart_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, MAIN_URL)

    def test_add_item_to_cart(self):
        request = self.manage_cart_items(self.prod1, 'add')
        response = add_to_cart(request)
        cart = self.get_cart()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.items_number, 1)

    def test_json_response_after_add_item(self):
        request = self.manage_cart_items(self.prod1, 'add')
        response = add_to_cart(request)
        content = {
            'product_qty': 1,
            'product_total': str(self.prod1.total_price),
            'cart_items': 1,
        }

        self.assertJSONEqual(str(response.content, encoding='utf8'), content)

    def test_remove_item_from_cart(self):
        add_to_cart(self.manage_cart_items(self.prod1, 'add'))

        cart = self.get_cart()
        self.assertEqual(cart.items_number, 1)

        request = self.manage_cart_items(self.prod1, 'remove')
        response = add_to_cart(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.items_number, 0)

    def test_json_response_after_remove_item(self):
        add_to_cart(self.manage_cart_items(self.prod1, 'add'))
        add_to_cart(self.manage_cart_items(self.prod1, 'add'))
        cart = self.get_cart()
        self.assertEqual(cart.items_number, 2)

        request = self.manage_cart_items(self.prod1, 'remove')
        response = add_to_cart(request)

        content = {
            'product_qty': 1,
            'product_total': str(self.prod1.total_price),
            'cart_items': 1,
        }

        self.assertJSONEqual(str(response.content, encoding='utf8'), content)

    def test_delete_item_from_cart(self):
        add_to_cart(self.manage_cart_items(self.prod1, 'add'))
        add_to_cart(self.manage_cart_items(self.prod2, 'add'))
        cart = self.get_cart()
        self.assertEqual(cart.items_number, 2)

        request = self.manage_cart_items(self.prod1, 'delete')
        response = add_to_cart(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.items_number, 1)
        self.assertEqual(float(cart.cart_total), self.prod2.total_price)

    def test_json_response_after_delete_item(self):
        add_to_cart(self.manage_cart_items(self.prod1, 'add'))
        add_to_cart(self.manage_cart_items(self.prod2, 'add'))
        cart = self.get_cart()
        self.assertEqual(cart.items_number, 2)

        request = self.manage_cart_items(self.prod1, 'delete')
        response = add_to_cart(request)
        content = {
            'product_qty': 0,
            'product_total': '0.00',
            'cart_items': 1,
        }

        self.assertJSONEqual(str(response.content, encoding='utf8'), content)

    def test_get_cart_data_empty_cart(self):
        request = self.create_request('GET', GET_CART_DATA)
        response = get_cart_data(request)

        self.assertEqual(response.status_code, 404)

    def test_cart_data_1_item(self):
        add_to_cart(self.manage_cart_items(self.prod1, 'add'))
        request = self.factory.get(GET_CART_DATA, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        request.user = self.user
        response = get_cart_data(request)

        content = {
            'cart_total': str(self.prod1.total_price),
            'cart_items': 1,
        }

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), content)

    def create_request(self, method, url, context=None):
        request = None
        if method == 'POST':
            request = self.factory.post(url, context)
            request.user = self.user
        elif method == 'GET':
            request = self.factory.get(url, context)
            request.user = self.user

        # Deal with messages middleware error
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request

    def manage_cart_items(self, product, action):
        data = {
            'productId': product.id,
            'action': action
        }
        return self.create_request('POST', ADD_TO_CART, data)

    def get_cart(self):
        return self.user.customer.cart_set.first()
