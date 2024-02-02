from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from .enums import PlanPeriod


class ConsumeEnergyDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    plan_period = models.CharField(
        choices=PlanPeriod.choices(), default=PlanPeriod.WEEK
    )
    period_execution = models.IntegerField(validators=[MinValueValidator(1)])


class StoreEnergyDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])


class ProduceEnergyDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
