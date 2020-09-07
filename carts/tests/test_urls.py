from django.test import TestCase
from django.urls import reverse, resolve
from carts.views import (cart_view,
                         add_to_cart,
                         get_cart_data,
                         CheckoutView,
                         CheckoutCompleted)


class TestCartUrls(TestCase):
    def test_cart_url_resolves(self):
        url = reverse('cart')
        self.assertEqual(resolve(url).func, cart_view)

    def test_add_to_cart_url_resolves(self):
        url = reverse('add-item')
        self.assertEqual(resolve(url).func, add_to_cart)

    def test_get_cart_data_url_resolves(self):
        url = reverse('cart-data')
        self.assertEqual(resolve(url).func, get_cart_data)

    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func.view_class, CheckoutView)

    def test_checkout_confirm_url_resolves(self):
        url = reverse('checkout-confirm')
        self.assertEqual(resolve(url).func.view_class, CheckoutCompleted)
