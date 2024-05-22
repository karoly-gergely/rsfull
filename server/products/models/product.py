from django.db import models

from server.common.models import AbstractBaseModel
from server.core.models import User
from server.products.enums import CurrencyChoices


class BaseProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


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
    deleted = models.BooleanField(default=False)

    objects = BaseProductManager()

    class Meta:
        ordering = ('datetime_created', )

    def __str__(self):
        return f"{self.id} - {self.name} - {self.currency}{self.price}" \
            if not self.deleted else f"DELETED by {self.user}"

    def delete(self, **kwargs):
        if not self.deleted:
            self.deleted = True
            self.save(update_fields=('deleted', ))
