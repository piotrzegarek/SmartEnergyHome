from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .consts import dev_type_to_form, dev_type_to_model


class DevicesView(LoginRequiredMixin, ListView):
    template_name = "devices/devices.html"
    context_object_name = "devices"

    def get_queryset(self) -> QuerySet[Any]:
        device_type = self.kwargs.get("dev_type")
        if device_type not in ["consume", "store", "produce"]:
            raise Http404("Object does not exist")

        query = (
            dev_type_to_model[device_type].objects.filter(user=self.request.user).all()
        )

        return query

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        device_type = self.kwargs.get("dev_type")
        context["type"] = device_type[0:-1] + "ing"

        return context


class DevicesAddPickView(LoginRequiredMixin, TemplateView):
    template_name = "devices/devices-add.html"


class DevicesAddView(LoginRequiredMixin, View):
    def get(self, request, dev_type):
        form = self._get_form(dev_type)

        return render(
            request,
            "devices/devices-add-form.html",
            {"form": form, "type": dev_type[0:-1] + "ing"},
        )

    def post(self, request, dev_type):
        form = self._get_form(dev_type)(request.POST, user=request.user)

        if form.is_valid():
            new_device = form.save(commit=False)
            new_device.user = request.user
            new_device.save()
            return redirect("devices-page", dev_type=dev_type)

        return render(
            request,
            "devices/devices-add-form.html",
            {"form": form, "type": dev_type[0:-1] + "ing"},
        )

    def _get_form(self, dev_type):
        try:
            form = dev_type_to_form[dev_type]
            return form
        except KeyError:
            raise Http404("Object does not exist")
