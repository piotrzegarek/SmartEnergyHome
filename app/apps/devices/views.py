import json
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .consts import dev_type_to_form, dev_type_to_model
from .exceptions import DeviceNotOwned, ObjectNotFound


class DevicesView(LoginRequiredMixin, ListView):
    template_name = "devices/devices.html"
    context_object_name = "devices"

    def get_queryset(self) -> QuerySet[Any]:
        device_type = self.kwargs.get("dev_type")
        if device_type not in ["consume", "store", "produce"]:
            raise Http404("Object does not exist")

        return dev_type_to_model[device_type].by_user(self.request.user)

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
            dev_type_to_model[dev_type].create(form, request.user)
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


class RemoveDevice(View):
    def delete(self, request):
        data = json.load(request)
        device_id = data.get("device_id")
        device_type = data.get("device_type")
        if device_id and device_type:
            try:
                dev_type_to_model[device_type].remove(device_id, request.user.id)
                return JsonResponse({"msg": "Device removed successfully."})
            except (ObjectNotFound, DeviceNotOwned):
                return JsonResponse({"msg": "Something went wrong."}, status=400)
        else:
            return JsonResponse({"msg": "Unvalid request."}, status=400)
