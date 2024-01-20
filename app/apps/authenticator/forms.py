from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError
from django.utils.translation import gettext_lazy as _


class UserCacheMixin:
    user_cache = None


class LoginForm(UserCacheMixin, ModelForm):
    pass


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data["email"]

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError(
                _("This email address already exists. Log in instead.")
            )

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password2
