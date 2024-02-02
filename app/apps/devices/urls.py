from django.urls import path

from . import views

urlpatterns = [
    path("<str:dev_type>", views.DevicesView.as_view(), name="devices-page"),
    path("add-pick/", views.DevicesAddPickView.as_view(), name="devices-add-page"),
    path("add/<str:dev_type>", views.DevicesAddView.as_view(), name="devices-add"),
]
