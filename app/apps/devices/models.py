from typing import List

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.forms import ModelForm

from .exceptions import DeviceNotOwned, ObjectNotFound


class Device(models.Model):
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
            if device.user.id == user_id:
                device.delete()
            else:
                raise DeviceNotOwned
        except AttributeError:
            raise ObjectNotFound

    @classmethod
    def by_user(cls, user: User) -> List["Device"]:
        return cls.objects.filter(user=user).all()

    class Meta:
        abstract = True


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
