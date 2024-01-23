from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "core/home-page.html")

    def post():
        pass


class DevicesView(LoginRequiredMixin, View):
    def get(self, request, dev_type):
        if dev_type not in ["consume", "store", "produce"]:
            raise Http404("Object does not exist")

        return render(
            request,
            "core/devices.html",
            {
                "type": dev_type,
            },
        )


class DevicesAddView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "core/devices-add.html")
