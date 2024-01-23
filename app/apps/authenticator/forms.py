from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class UserCacheMixin:
    user_cache = None


class LoginForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_("Email or Username"))
    password = forms.CharField(
        label=_("Password"), strip=False, widget=forms.PasswordInput
    )
    remember_me = forms.BooleanField(label="Remember me", required=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == "remember_me":
                self.fields[field].widget.attrs.update({"class": "form-check-input"})
            else:
                self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean_password(self):
        password = self.cleaned_data["password"]

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_("You entered an invalid password."))

        return password

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data["email_or_username"]

        user = User.objects.filter(
            Q(username=email_or_username) | Q(email__iexact=email_or_username)
        ).first()
        if not user:
            raise ValidationError(
                _("You entered an invalid email address or username.")
            )

        self.user_cache = user

        return email_or_username


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
