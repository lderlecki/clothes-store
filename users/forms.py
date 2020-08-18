from django import forms
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Customer


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat password'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class CustomerDataForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone',)

    # def save(self, user):
    #     customer = user.customer
    #     first_name = self.cleaned_data['first_name']
    #     last_name = self.cleaned_data['last_name']
    #     phone = self.cleaned_data['phone']
    #     email = self.cleaned_data['email']
    #     user.set_password(password)
    #     user.save()


class SetNewPasswordForm(ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    new_password = forms.CharField(required=False, widget=forms.PasswordInput())
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['new_password'].widget.attrs['placeholder'] = 'New password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Repeat password'

    class Meta:
        model = User
        fields = ('password', 'confirm_password',)

    def clean_password(self, *args, **kwargs):
        data = self.cleaned_data
        if self.user.check_password(data.get('password')):
            return data['password']
        raise forms.ValidationError("Password is incorrect.")

    def clean(self, *args, **kwargs):
        cleaned_data = super(SetNewPasswordForm, self).clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError({'new_password': 'New passwords must match each other.'})
        if not bool(new_password and confirm_password):
            raise forms.ValidationError({'new_password': 'Password cannot be empty.'})

        validate_password(new_password)
        return cleaned_data

    def save(self, user):
        password = self.cleaned_data['new_password']
        user.set_password(password)
        user.save()
