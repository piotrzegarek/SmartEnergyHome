from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class ConsumeEnergyDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    energy_consumption = models.FloatField(validators=[MinValueValidator(0)])
    energy_unit = models.CharField(max_length=10)
    period_execution = models.IntegerField(validators=[MinValueValidator(1)])
    plan_period = models.CharField(max_length=120)
    enabled = models.BooleanField(default=True)


class StoreEnergyDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    enabled = models.BooleanField(default=True)


class ProduceEnergyDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    enabled = models.BooleanField(default=True)
