from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Company
from .serializers import CompanySerializer, RegisterSerializer

# Tests for the Company Model
class CompanyModelTest(TestCase):
    """ Test module for Company model """

    def setUp(self):
        self.company = Company.objects.create(
            name='Test Company',
            website='http://test.com',
            foundation='2022-02-15'
        )

    def test_company_str(self):
        self.assertEqual(str(self.company), self.company.name)


class CompanyViewTestCase(APITestCase):
    """ Test module for Company views """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.company_data = {'name': 'Test Company', 'website': 'http://test.com', 'foundation': '2022-02-15'}

    def test_create_company(self):
        response = self.client.post(reverse('company_view'), self.company_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_company(self):
        company = Company.objects.create(name='Test Company', website='http://test.com', foundation='2022-02-15')
        updated_company_data = {'name': 'Test Company Updated', 'website': 'http://test-updated.com', 'foundation': '2022-02-16'}
        response = self.client.put(reverse('company_view', args=[company.id]), updated_company_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_company(self):
        company = Company.objects.create(name='Test Company', website='http://test.com', foundation='2022-02-15')
        response = self.client.delete(reverse('company_view', args=[company.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CompanySerializerTest(TestCase):
    """ Test module for Company serializer """

    def setUp(self):
        self.company_data = {'name': 'Test Company', 'website': 'http://test.com', 'foundation': '2022-02-15'}
        self.serializer = CompanySerializer(data=self.company_data)

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_data(self):
        company_data = {'name': '', 'website': 'http://test.com', 'foundation': '2022-02-15'}
        serializer = CompanySerializer(data=company_data)
        self.assertFalse(serializer.is_valid())


class RegisterSerializerTest(TestCase):
    """ Test module for Register serializer """

    def setUp(self):
        self.user_data = {'username': 'testuser', 'password': 'testpass', 'password2': 'testpass', 'email': 'test@test.com'}
        self.serializer = RegisterSerializer(data=self.user_data)

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_data(self):
        user_data = {'username': 'testuser', 'password': 'test', 'password2': 'test', 'email': 'test@test.com'}
        serializer = RegisterSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())
