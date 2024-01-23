from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .enums import PlanPeriod


class EnergyPrice(models.Model):
    date = models.DateField()
    hour = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)])
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.price}"


class ConsumeEnergyDevice(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    plan_period = models.CharField(
        choices=PlanPeriod.choices(), default=PlanPeriod.WEEK
    )
    period_execution = models.IntegerField(validators=[MinValueValidator(1)])

    def save(self, *args, **kwargs):
        # Check if there is an existing ConsumeEnergyDevice with the same name
        if ConsumeEnergyDevice.objects.filter(name=self.name, user=self.user).exists():
            raise ValidationError("Device with this name already exists for the user.")

        super().save(*args, **kwargs)


class StoreEnergyDevice(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

    def save(self, *args, **kwargs):
        # Check if there is an existing StoreEnergyDevice with the same name
        if StoreEnergyDevice.objects.filter(name=self.name, user=self.user).exists():
            raise StoreEnergyDevice(
                "Device with this name already exists for the user."
            )

        super().save(*args, **kwargs)


class ProduceEnergyDevice(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

    def save(self, *args, **kwargs):
        # Check if there is an existing ProduceEnergyDevice with the same name
        if ProduceEnergyDevice.objects.filter(name=self.name, user=self.user).exists():
            raise ProduceEnergyDevice(
                "Device with this name already exists for the user."
            )

        super().save(*args, **kwargs)
