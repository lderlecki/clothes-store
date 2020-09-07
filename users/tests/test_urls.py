from django.test import TestCase
from django.urls import reverse, resolve
from users.views import (loginView,
                         logoutView,
                         registerView,
                         accountView,
                         editAccountView,
                         orderHistoryView,
                         addressAccountView,
                         addressAddView,
                         )


class TestCartUrls(TestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, loginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logoutView)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, registerView)

    def test_account_url_resolves(self):
        url = reverse('account')
        self.assertEqual(resolve(url).func, accountView)

    def test_edit_account_url_resolves(self):
        url = reverse('account-edit')
        self.assertEqual(resolve(url).func, editAccountView)

    def test_order_history_url_resolves(self):
        url = reverse('order-history')
        self.assertEqual(resolve(url).func, orderHistoryView)

    def test_address_account_url_resolves(self):
        url = reverse('address-list')
        self.assertEqual(resolve(url).func, addressAccountView)

    def test_address_add_url_resolves(self):
        url = reverse('address-add')
        self.assertEqual(resolve(url).func, addressAddView)
