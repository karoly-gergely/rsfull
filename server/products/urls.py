from django.urls import path

from server.products.views import (ProductDetailUpdateDestroyView,
                                   ProductListCreateView)

app_name = "products"

urlpatterns = [
    path(
        "api/products/", ProductListCreateView.as_view(), name="list-create"
    ),
    path(
        "api/products/<str:pk>/",
        ProductDetailUpdateDestroyView.as_view(),
        name="detail-update-destroy"
    ),
]
