from django.urls import path

from server.products.views import ProductsListCreateView

app_name = "products"

urlpatterns = [
    path("api/products/", ProductsListCreateView.as_view(), name="list-create")
]
