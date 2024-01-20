from typing import Any

from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, View

from .forms import LoginForm, RegisterForm


class GuestOnlyView(View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect("home-page")

        return super().dispatch(request, *args, **kwargs)


class LoginView(GuestOnlyView, FormView):
    template_name = "authenticator/login.html"
    form_class = LoginForm

    @method_decorator(sensitive_post_parameters("password"))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # If the test cookie worked, go ahead and delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        if not form.cleaned_data["remember_me"]:
            self.request.session.set_expiry(0)

        login(self.request, form.user_cache)

        redirect_to = self.request.POST.get(
            REDIRECT_FIELD_NAME, self.request.GET.get(REDIRECT_FIELD_NAME)
        )
        url_is_safe = is_safe_url(
            redirect_to,
            allowed_hosts=self.request.get_host(),
            require_https=self.request.is_secure(),
        )

        if url_is_safe:
            return redirect(redirect_to)

        return redirect("home-page")


class RegisterView(GuestOnlyView, FormView):
    template_name = "authenticator/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home-page")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        self.request.session.set_expiry(0)
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("login")
