from decimal import Decimal

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
        self.assertNotIn('description', response.data['results'][0])
        self.client.logout()
        print("Logged-in User with results PASSED")

    def test_create(self):
        """Product will be created for the current
        user only if authenticated and data is valid"""

        valid_name = 'name'

        # Anon User
        data = {
            'name': '',
            'price': Decimal('1.00'),
            'currency': '$',
            'description': '',
        }
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Anon User PASSED")

        # Logged-in User1 but missing name
        data = {
            'price': Decimal('1.00'),
            'currency': '$',
            'description': 'Some descr',
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 but missing name PASSED")

        # Logged-in User1 invalid price
        data = {
            'name': valid_name,
            'price': Decimal('-1.00'),
            'currency': '$',
            'description': 'Some descr',
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 invalid price PASSED")

        # Logged-in User1 invalid currency
        data = {
            'name': valid_name,
            'price': Decimal('1.00'),
            'currency': 'RON',
            'description': 'Some descr',
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 invalid currency PASSED")

        # Logged-in User1 trying to override user
        data = {
            'name': valid_name,
            'price': Decimal('1.00'),
            'currency': '$',
            'description': 'Some descr',
            'user': 1
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], valid_name)
        self.assertEqual(response.data['user']['id'], str(self.user1.id))
        self.client.logout()
        print("Logged-in User1 trying to override user PASSED")

        # Logged-in User1 success
        data = {
            'name': valid_name,
            'price': Decimal('1.00'),
            'currency': '$',
            'description': 'Some descr',
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], valid_name)
        self.assertEqual(response.data['user']['id'], str(self.user1.id))
        self.client.logout()
        print("Logged-in User1 success PASSED")

        # Logged-in User1 success descr missing
        data = {
            'name': valid_name,
            'price': Decimal('1.00'),
            'currency': '$',
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], valid_name)
        self.assertEqual(response.data['user']['id'], str(self.user1.id))
        self.client.logout()
        print("Logged-in User1 success descr missing PASSED")

        # Logged-in User2 success
        data = {
            'name': valid_name,
            'price': Decimal('1.00'),
            'currency': '$',
            'description': 'Some descr',
        }

        self.client.login(email=self.user2.email, password=self.user_password)
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], valid_name)
        self.assertEqual(response.data['user']['id'], str(self.user2.id))
        self.client.logout()
        print("Logged-in User2 success PASSED")

    def test_retrieve(self):
        """Product will be retrieved for the current
        user only if authenticated"""

        # Anon User
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Anon User PASSED")

        # Logged-in user but wrong user
        self.client.login(email=self.user2.email, password=self.user_password)
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        print("Logged-in user but wrong user PASSED")

        # Logged-in user with correct user
        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.base_product.id))
        self.assertEqual(response.data['name'], self.base_product.name)
        self.assertIn('description', response.data)
        self.assertEqual(response.data['user']['id'], str(self.user1.id))
        self.assertNotIn('email', response.data['user'])
        self.client.logout()
        print("Logged-in user with correct user PASSED")

    def test_patch(self):
        """Product will be patched and retrieved for the current
        user only if authenticated and owned"""

        valid_data = {
            'name': 'NewName',
            'description': 'NewDescr',
            'price': Decimal('100.23'),
            'currency': '$'
        }

        # Anon User
        data = {
            'name': '',
        }
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Anon User PASSED")

        # Logged-in User2 wrong user
        data = {
            'name': ''
        }

        self.client.login(email=self.user2.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        print("Logged-in User2 wrong user PASSED")

        # Logged-in User1 empty name
        data = {
            'name': ''
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 empty name PASSED")

        # Logged-in User1 invalid price
        data = {
            'price': Decimal('-1.23')
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 invalid price PASSED")

        # Logged-in User1 invalid currency
        data = {
            'currency': ''
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 invalid currency PASSED")

        # Logged-in User1 trying to override user
        data = {
            'user': 1
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], str(self.user1.id))
        self.client.logout()
        print("Logged-in User1 trying to override user PASSED")

        # Logged-in User1 success
        data = {
            'name': valid_data['name'],
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], valid_data['name'])
        self.client.logout()
        print("Logged-in User1 success PASSED")

        # Logged-in User1 success multiple items
        data = {
            'name': valid_data['name'],
            'price': valid_data['price'],
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], valid_data['name'])
        self.assertEqual(response.data['price'], '100.23')
        self.client.logout()
        print("Logged-in User1 success multiple items PASSED")

        # Logged-in User1 success multiple items with error
        data = {
            'name': valid_data['name'],
            'price': valid_data['price'],
            'currency': 2,
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 success multiple items with error PASSED")

        # Logged-in User1 success multiple items with multiple error
        data = {
            'name': valid_data['name'],
            'price': 'asd',
            'currency': 2,
            'description': 'test',
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(list(response.data.keys())), 2)
        self.client.logout()
        print(
            "Logged-in User1 success multiple "
            "items with multiple error PASSED"
        )

    def test_put(self):
        """Product will be updated and retrieved for the current
        user only if authenticated and owned"""

        valid_data = {
            'name': 'NewName',
            'description': 'NewDescr ',
            'price': Decimal('100.23'),
            'currency': '$'
        }

        # Anon User
        data = {
            'name': '',
        }
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Anon User PASSED")

        # Logged-in User2 wrong user
        data = {
            'name': ''
        }

        self.client.login(email=self.user2.email, password=self.user_password)
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        print("Logged-in User2 wrong user PASSED")

        # Logged-in User1 empty name
        data = {
            'description': 'NewDescr',
            'price': Decimal('100.23'),
            'currency': '$'
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 empty name PASSED")

        # Logged-in User1 invalid price
        data = {
            'name': 'NewName',
            'description': 'NewDescr',
            'price': Decimal('-100.23'),
            'currency': '$'
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 invalid price PASSED")

        # Logged-in User1 invalid currency
        data = {
            'name': 'NewName',
            'description': 'NewDescr',
            'price': Decimal('100.23'),
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 invalid currency PASSED")

        # Logged-in User1 trying to override user
        data = {
            'name': 'NewName',
            'description': 'NewDescr',
            'price': Decimal('100.23'),
            'currency': '$',
            'user': 1,
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], valid_data['name'])
        self.assertEqual(response.data['user']['id'], str(self.user1.id))
        self.client.logout()
        print("Logged-in User1 trying to override user PASSED")

        # Logged-in User1 success
        data = {
            'name': valid_data['name'],
            'description': self.base_product.description,
            'price': self.base_product.price,
            'currency': self.base_product.currency,
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], valid_data['name'])
        self.assertEqual(
            response.data['price'], str(self.base_product.price)
        )
        self.assertEqual(
            response.data['currency'], self.base_product.currency
        )
        self.assertEqual(
            response.data['description'], self.base_product.description
        )
        self.client.logout()
        print("Logged-in User1 success PASSED")

        # Logged-in User1 success multiple items
        data = {
            'name': valid_data['name'],
            'description': valid_data['description'],
            'price': self.base_product.price,
            'currency': self.base_product.currency,
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], valid_data['name'])
        self.assertEqual(
            response.data['description'], valid_data['description'].strip()
        )
        self.assertEqual(
            response.data['price'], str(self.base_product.price)
        )
        self.assertEqual(
            response.data['currency'], self.base_product.currency
        )
        self.client.logout()
        print("Logged-in User1 success multiple items PASSED")

        # Logged-in User1 success multiple items with error
        data = {
            'name': valid_data['name'],
            'description': valid_data['description'],
            'price': 'sdadsads',
            'currency': self.base_product.currency,
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        print("Logged-in User1 success multiple items with error PASSED")

        # Logged-in User1 success multiple items with multiple error
        data = {
            'name': valid_data['name'],
            'description': valid_data['description'],
            'price': 'sdaasddas',
            'currency': 2,
        }

        self.client.login(email=self.user1.email, password=self.user_password)
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(list(response.data.keys())), 2)
        self.client.logout()
        print(
            "Logged-in User1 success multiple "
            "items with multiple error PASSED"
        )

    def test_delete(self):
        """Product will be soft deleted for the current
        user only if authenticated and owned"""

        # Anon User
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Anon User PASSED")

        # Logged-in User2 wrong user
        self.client.login(email=self.user2.email, password=self.user_password)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        print("Logged-in User2 wrong user PASSED")

        def one_successful_pass(is_first_pass=True):
            self.client.login(
                email=self.user1.email, password=self.user_password
            )
            self.base_product.refresh_from_db()
            self.assertFalse(
                self.base_product.deleted if is_first_pass
                else not self.base_product.deleted
            )
            response = self.client.delete(self.url_detail)
            self.assertEqual(
                response.status_code,
                status.HTTP_204_NO_CONTENT if is_first_pass
                else status.HTTP_404_NOT_FOUND
            )
            self.base_product.refresh_from_db()
            self.assertIsNotNone(self.base_product)
            self.assertIsNotNone(self.base_product.id)
            self.assertTrue(self.base_product.deleted)
            response = self.client.get(self.url_detail)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            response = self.client.get(self.url_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 0)
            response = self.client.patch(
                self.url_detail, data={'name': 'test'}
            )
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.client.logout()

            # Ensure no permission issues over soft deleted content
            self.client.login(
                email=self.user2.email, password=self.user_password
            )
            response = self.client.get(self.url_detail)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.client.logout()

        # Logged-in User1 success
        one_successful_pass()
        print("Logged-in User1 success PASSED")

        # Logged-in User1 second pass success
        one_successful_pass(is_first_pass=False)
        print("Logged-in User1 second pass success PASSED")

    def tearDown(self):
        self.client.logout()
