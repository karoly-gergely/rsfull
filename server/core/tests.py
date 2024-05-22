from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class UserRegistrationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("core:register")
        cls.valid_user_email = "mail@mail.com"
        cls.valid_user_password = "12345678"

    def test_registration(self):
        """User will be created with valid data and not otherwise"""

        # Invalid email & password & other fields optional but less than 255
        data = {
            'email': '',
            'password': '',
            'first_name': 'nsadlkldsakndsaldnlsakndlksndsandlfnlfsanlflkasfnfafsafslkngklngaslsgnlgsaknngaslkasgn'
                          'gsalkgnlsganlksagnlagsngaslngaslkngslkgasnglknalkgnslnglkasnglknglkasnglsnsaglngasnlsglsna'
                          'sk agk sg glnglnaslgnglanlgknsalknglkansglasnglasnglkasnglsanglsanglkslknglsanglksnglsa'
                          'asjksanlkgnaslkgnaslnglkgnlskgnlsalgnglaksnlgsalnglasnlasnglkasnglnsglsnaglksangalskngl',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data.keys()), 3)
        print("Invalid email & password & other fields optional but less than 255 PASSED")

        # Invalid email & valid password & other fields optional but less than 255
        data = {
            'email': 'mail@mail',
            'password': self.valid_user_password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data.keys()), 1)
        self.assertEqual(response.data['email'][0], "Enter a valid email address.")
        print("Invalid email & valid password & other fields optional but less than 255 PASSED")

        # Valid email & invalid password & other fields optional but less than 255 - Stage 1
        data = {
            'email': self.valid_user_email,
            'password': 'asd',
            'first_name': 'nsadlkldsakndsaldnlsakndlksndsandlfnlfsanlflkasfnfafsafslkngklngaslsgnlgsaknngaslkasgn'
                          'gsalkgnlsganlksagnlagsngaslngaslkngslkgasnglknalkgnslnglkasnglknglkasnglsnsaglngasnlsglsna'
                          'sk agk sg glnglnaslgnglanlgknsalknglkansglasnglasnglkasnglsanglsanglkslknglsanglksnglsa'
                          'asjksanlkgnaslkgnaslnglkgnlskgnlsalgnglaksnlgsalnglasnlasnglkasnglnsglsnaglksangalskngl',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data.keys()), 1)
        self.assertEqual(response.data['first_name'][0],
                         "Ensure this field has no more than 255 characters.")
        print("Valid email & invalid password & other fields optional but less than 255 - Stage 1 PASSED")

        # Valid email & invalid password & other fields optional but less than 255 - Stage 2
        data = {
            'email': self.valid_user_email,
            'password': 'asd',
            'first_name': 'asjksanlkgnaslkgnaslnglkgnlskgnlsalgnglaksnlgsalnglasnlasnglkasnglnsglsnaglksangalskngl',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data.keys()), 1)
        self.assertEqual(response.data['non_field_errors'][0],
                         "This password is too short. It must contain at least 8 characters.")
        print("Valid email & invalid password & other fields optional but less than 255 - Stage 2 PASSED")

        # Valid email & password & other fields optional but less than 255 (Success & Login)
        data = {
            'email': self.valid_user_email,
            'password': self.valid_user_password,
            'first_name': 'mike',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data.keys()), 6)
        self.assertEqual(response.data['first_name'], "mike")
        self.assertEqual(response.data['email'], self.valid_user_email)
        self.assertIn("token", list(response.data.keys()))
        print("Valid email & password & other fields optional but less than 255 PASSED")
