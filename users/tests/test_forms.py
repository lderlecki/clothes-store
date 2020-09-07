from django.contrib.auth.models import User
from django.test import TestCase
from users.forms import (
    AddressForm,
    SetNewPasswordForm,
    CustomerDataForm,
    CreateUserForm,
    AnonymousAddressForm,
)


class TestUserForms(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('testuser123', password='testing321')

    def test_create_user_form_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testing321',
            'password2': 'testing321',
        }
        form = CreateUserForm(data)

        self.assertTrue(form.is_valid())

    def test_create_user_form_no_data(self):
        form = CreateUserForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_create_user_form_invalid_email(self):
        data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'testing321',
            'password2': 'testing321',
        }
        form = CreateUserForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_customer_data_form_valid_data(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test@test.com',
            'phone': '999888777',
        }
        form = CustomerDataForm(data)
        self.assertTrue(form.is_valid())

    def test_customer_data_form_no_data(self):
        form = CustomerDataForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_customer_data_form_invalid_email(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test@test',
            'phone': '999888777',
        }
        form = CustomerDataForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_set_new_password_form_valid_data(self):
        data = {
            'password': 'testing321',
            'new_password': 'somenewpasword321',
            'confirm_password': 'somenewpasword321'
        }
        form = SetNewPasswordForm(data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_set_new_password_form_valid_data_save_form(self):
        data = {
            'password': 'testing321',
            'new_password': 'somenewpasword321',
            'confirm_password': 'somenewpasword321'
        }
        form = SetNewPasswordForm(data, user=self.user)
        if form.is_valid():
            form.save(self.user)
            self.assertTrue(self.user.check_password('somenewpasword321'))
        else:
            self.fail('Set new password form is not valid')

    def test_set_new_password_form_invalid_confirm_password(self):
        data = {
            'password': 'testing321',
            'new_password': 'somenewpasword321',
            'confirm_password': 'invalidpassword'
        }
        form = SetNewPasswordForm(data, user=self.user)
        self.assertFalse(form.is_valid())
        errors = dict(form.errors)
        self.assertEqual(errors.get('new_password'), ['New passwords must match each other.'])
        self.assertEqual(len(form.errors), 1)

    def test_set_new_password_form_no_new_and_confirm_password(self):
        data = {
            'password': 'testing321',
            'new_password': '',
            'confirm_password': ''
        }
        form = SetNewPasswordForm(data, user=self.user)
        self.assertFalse(form.is_valid())
        errors = dict(form.errors)
        self.assertEqual(errors.get('new_password'), ['Password cannot be empty.'])
        self.assertEqual(len(form.errors), 1)

    def test_set_new_password_form_not_safe_password(self):
        data = {
            'password': 'testing321',
            'new_password': 'test',
            'confirm_password': 'test'
        }
        form = SetNewPasswordForm(data, user=self.user)
        self.assertFalse(form.is_valid())

        # Two errors, but one error class
        self.assertEqual(len(form.errors.items()), 1)

    def test_set_new_password_form_invalid_old_password_valid_new_and_confirm_password(self):
        data = {
            'password': 'invalidpassword',
            'new_password': 'newpassword321',
            'confirm_password': 'newpassword321'
        }
        form = SetNewPasswordForm(data, user=self.user)
        self.assertFalse(form.is_valid())
        errors = dict(form.errors)
        self.assertEqual(errors.get('password'), ['Password is incorrect.'])
        self.assertEqual(len(form.errors), 1)

    def test_address_form_valid_data(self):
        data = {
            'name': 'AddressName', 'first_name': 'John', 'last_name': 'Smith',
            'company_name': '', 'tax_number': '', 'street': 'Street',
            'number': '123', 'zip_code': '99-999', 'city': 'Warsaw',
            'country': 'Poland', 'phone': '999-888-777', 'default': True, 'address_type': 'B'
        }
        form = AddressForm(data)
        self.assertTrue(form.is_valid())

    def test_address_form_no_data(self):
        form = AddressForm(data={})
        self.assertFalse(form.is_valid())

    def test_anonymous_address_form_valid_data(self):
        data = {
            'name': 'AddressName', 'first_name': 'John', 'last_name': 'Smith',
            'company_name': '', 'tax_number': '', 'street': 'Street',
            'number': '123', 'zip_code': '99-999', 'city': 'Warsaw',
            'country': 'Poland', 'phone': '999-888-777', 'default': True, 'address_type': 'B'
        }
        form = AnonymousAddressForm(data)
        self.assertTrue(form.is_valid())

    def test_anonymous_address_form_no_data(self):
        form = AnonymousAddressForm(data={})
        self.assertFalse(form.is_valid())
