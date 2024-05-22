from django.db import models

from server.common.models import AbstractBaseModel
from server.core.models import User
from server.products.enums import CurrencyChoices


class Product(AbstractBaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(
        max_length=16,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD
    )

    class Meta:
        ordering = ('datetime_created', )

    def __str__(self):
        return f"{self.id} - {self.name} - {self.currency}{self.price}"
