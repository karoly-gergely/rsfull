from django.contrib import admin

from server.products.models import ImageInstance, Product

admin.site.register(Product)
admin.site.register(ImageInstance)
