from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class LoginForm(ModelForm):
    pass


class RegisterForm(ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
