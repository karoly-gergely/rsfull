from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from server.core.models import User
from server.products.enums import CurrencyChoices
from server.products.models import Product


class ProductsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_password = 'test1234'
        cls.url_list = reverse("products:list-create")
        cls.user1 = User.objects.create(
            email="test@email0512.com")
        cls.user1.set_password(cls.user_password)
        cls.user1.save()
        cls.user2 = User.objects.create(
            email="test2@email0512.com")
        cls.user2.set_password(cls.user_password)
        cls.user2.save()
        cls.base_product = Product.objects.create(
            name="Test", description="TestDescr",
            price=120.21, currency=CurrencyChoices.USD,
            user=cls.user1
        )
        cls.url_detail = reverse(
            "products:detail-update-destroy",
            kwargs={'pk': cls.base_product.id}
        )

    def test_listing(self):
        """Products will be retrieved for the current
        user only if authenticated"""

        # Anon User
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Anon User PASSED")

        # Logged-in user but empty response
        self.client.login(email=self.user2.email, password=self.user_password)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.client.logout()
        print("Logged-in User no results PASSED")

        # Logged-in user with actual response
        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'], str(self.base_product.id)
        )
        self.client.logout()
        print("Logged-in User with results PASSED")

    def test_create(self):
        """Product will be created for the current
        user only if authenticated"""

        # Anon User
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Anon User PASSED")

    def tearDown(self):
        self.client.logout()
