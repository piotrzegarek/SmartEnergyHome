from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

# from django.shortcuts import render
from django.views import View


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse("Hello test")

    def post():
        pass
