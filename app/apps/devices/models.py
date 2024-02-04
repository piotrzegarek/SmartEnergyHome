from typing import List

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.forms import ModelForm

from .exceptions import DeviceNotOwned, InvalidForm, ObjectNotFound


class Device(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    enabled = models.BooleanField(default=True)

    @classmethod
    def create(cls, form: ModelForm, user: User):
        new_device = form.save(commit=False)
        new_device.user = user
        new_device.save()

    @classmethod
    def remove(cls, device_id: int, user_id: int):
        try:
            device = cls.objects.filter(id=device_id).first()
            if device.user.id != user_id:
                raise DeviceNotOwned

            device.delete()
        except AttributeError:
            raise ObjectNotFound

    @classmethod
    def update(cls, device_id: int, user: User, data: dict, form):
        device = cls.by_id(device_id)
        if device.user.id != user.id:
            raise DeviceNotOwned

        form_updated = form(data, instance=device, id=device.id, user=user)
        if not form_updated.is_valid():
            raise InvalidForm(errors=form_updated.errors)

        form_updated.save()

    @classmethod
    def by_user(cls, user: User) -> List["Device"]:
        return cls.objects.filter(user=user).all()

    @classmethod
    def by_id(cls, id: int) -> "Device":
        device = cls.objects.filter(id=id).first()
        if not device:
            raise ObjectNotFound

        return device


class ConsumeEnergyDevice(Device):
    energy_consumption = models.FloatField(validators=[MinValueValidator(0)])
    energy_unit = models.CharField(max_length=10)
    period_execution = models.IntegerField(validators=[MinValueValidator(1)])
    plan_period = models.CharField(max_length=120)


class StoreEnergyDevice(Device):
    capacity = models.IntegerField(validators=[MinValueValidator(0)])
    capacity_unit = models.CharField(max_length=10)


class ProduceEnergyDevice(Device):
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    capacity_unit = models.CharField(max_length=10)
