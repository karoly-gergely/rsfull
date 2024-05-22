from rest_framework import generics


class ProductsListCreateView(generics.ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
