from django.urls import path

from . import views

urlpatterns = [
    path("delete", views.RemoveDevice.as_view(), name="devices-remove"),
    path("add-pick/", views.DevicesAddPickView.as_view(), name="devices-add-page"),
    path("add/<str:dev_type>", views.DevicesAddView.as_view(), name="devices-add"),
    path("<str:dev_type>", views.DevicesView.as_view(), name="devices-page"),
]
