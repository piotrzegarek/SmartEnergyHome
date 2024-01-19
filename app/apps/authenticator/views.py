from typing import Any

from django.http import HttpRequest
from django.shortcuts import redirect
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

    def form_valid(self, form):
        # request = self.request
        user = form.save(commit=False)

        user.username = form.cleaned_data["username"]
        user.save()
