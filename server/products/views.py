from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from server.products.models import Product
from server.products.serializers import ProductListSerializer


class ProductsListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            user=self.request.user
        )
