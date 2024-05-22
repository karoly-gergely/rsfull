from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"", include("server.core.urls", namespace="core")),
    path(r"", include("server.products.urls", namespace="products")),
]
