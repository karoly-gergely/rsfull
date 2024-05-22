import os

from django.db import models
from django.db.models import Model
from django.dispatch import receiver

from server.common.models import AbstractBaseModel
from server.products.models.product import Product
from server.settings import IN_PROD, IN_STAGING
from server.utils import custom_fields


class ImageInstance(AbstractBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    s3_image = custom_fields.UrlRetrieveOnlyFileField(upload_to='images',
                                                      null=True,
                                                      blank=True)

    class Meta:
        ordering = ('datetime_created', )

    def __str__(self):
        return f"Image {self.id}, {self.s3_image} || {self.product}"

    def __eq__(self, other):
        if not isinstance(other, Model):
            return False
        if self._meta.concrete_model != other._meta.concrete_model:
            return False
        my_pk = self.pk
        if my_pk is None:
            return self is other
        return my_pk == other.pk

    def __hash__(self):
        return super().__hash__()


@receiver(models.signals.post_delete, sender=ImageInstance)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `ImageInstance` object is deleted.
    """
    if instance.s3_image:
        if IN_PROD or IN_STAGING:
            instance.s3_image.delete(save=False)
        else:
            if os.path.isfile(instance.s3_image.path):
                os.remove(instance.s3_image.path)
