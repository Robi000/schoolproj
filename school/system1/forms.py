from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import AuthenticationForm


from .models import User


class my_user_form(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name',  'last_name', 'username', 'admin',
                  'phone_no', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "F_name"})
        self.fields['last_name'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "L_name"})
        self.fields['username'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "Username"})
        self.fields['admin'].widget.attrs.update(
            {'class': "form-check-input my-2"})
        self.fields['phone_no'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "09********"})
        self.fields['password1'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "Password"})
        self.fields['password2'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "C.password"})


class UserauthForm(AuthenticationForm):

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "password"})
        self.fields['password'].widget.attrs.update(
            {'class': "form-control my-2", "placeholder": "password"})
