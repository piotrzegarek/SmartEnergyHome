from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class EnergyPrice(models.Model):
    date = models.DateField()
    hour = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)])
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.price}"
