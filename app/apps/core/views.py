from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "core/home-page.html")

    def post():
        pass
