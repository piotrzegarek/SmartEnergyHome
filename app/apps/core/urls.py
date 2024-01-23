from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home-page"),
    path("devices/add", views.DevicesAddView.as_view(), name="devices-add-page"),
    path("devices/<str:dev_type>", views.DevicesView.as_view(), name="devices-page"),
]
