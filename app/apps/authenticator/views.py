from typing import Any

from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from .forms import RegisterForm


class GuestOnlyView(View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect("home-page")

        return super().dispatch(request, *args, **kwargs)


class RegisterView(GuestOnlyView, FormView):
    template_name = "authenticator/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home-page")  # adjust this URL as needed

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        self.request.session.set_expiry(0)
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super().form_valid(form)
