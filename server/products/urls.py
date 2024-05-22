from django.urls import path

from server.products.views import (ProductsDetailUpdateView,
                                   ProductsListCreateView)

app_name = "products"

urlpatterns = [
    path(
        "api/products/", ProductsListCreateView.as_view(), name="list-create"
    ),
    path(
        "api/products/<str:pk>/",
        ProductsDetailUpdateView.as_view(),
        name="detail-update"
    ),
]
