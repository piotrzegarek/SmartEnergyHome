from django.db import models

# Create your models here.


class EnergyPrice(models.Model):
    date = models.DateField(auto_now_add=True)
    hour = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.price}"
