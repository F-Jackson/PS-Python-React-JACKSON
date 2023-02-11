import json

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


client = APIClient()

valid_json = {
    "username": "test",
    "password": "123",
    "email": "test@test.com",
}


class UserCreateTestCase(TestCase):
    def setUp(self):
        self.valid_payload = valid_json

    def test_valid(self):
        response = client.put(
            reverse('user_view'),
            self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_has_already_has_username(self):
        response_ok = client.put(
            reverse('user_view'),
            self.valid_payload,
            format='json'
        )

        payload_error = {
            'username': self.valid_payload['username'],
            'email': 'test2@test.com',
            'password': '123'
        }

        response_error = client.put(
            reverse('user_view'),
            payload_error,
            format='json'
        )
        self.assertEqual(response_error.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_has_already_has_email(self):
        response_ok = client.put(
            reverse('user_view'),
            self.valid_payload,
            format='json'
        )

        payload_error = {
            'username': 'test2',
            'email': self.valid_payload['email'],
            'password': '123'
        }

        response_error = client.put(
            reverse('user_view'),
            payload_error,
            format='json'
        )
        self.assertEqual(response_error.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_xss_attack(self):
        invalid_payload = {
            'username': '<script></script>',
            'email': 'test@test.com',
            'password': '123'
        }

        response_error = client.put(
            reverse('user_view'),
            invalid_payload,
            format='json'
        )
        self.assertEqual(response_error.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_xss_attack(self):
        invalid_payload = {
            'username': 'test',
            'email': '<script>@test.com',
            'password': '123'
        }

        response_error = client.put(
            reverse('user_view'),
            invalid_payload,
            format='json'
        )
        self.assertEqual(response_error.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.valid_payload = valid_json
        client.put(
            reverse('user_view'),
            self.valid_payload,
            format='json'
        )

    def test_valid_login(self):
        response = client.post(
            reverse('user_view'),
            self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_username_login(self):
        invalid_payload = {
            'username': 'invalid',
            'email': self.valid_payload['email'],
            'password': self.valid_payload['password']
        }

        response = client.post(
            reverse('user_view'),
            invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_password_login(self):
        invalid_payload = {
            'username': self.valid_payload['username'],
            'email': self.valid_payload['email'],
            'password': '12'
        }

        response = client.post(
            reverse('user_view'),
            invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_success_token_retrive(self):
        response = client.post(
            reverse('user_view'),
            self.valid_payload,
            format='json'
        )
        self.assertIn('token', response.json())

    def test_user_success_token_retrive_type(self):
        response = client.post(
            reverse('user_view'),
            self.valid_payload,
            format='json'
        )
        token = response.json()['token']
        self.assertIsInstance(token, str)


class UserGetInfoTestCase(TestCase):
    def setUp(self):
        client.put(
            reverse('user_view'),
            valid_json,
            format='json'
        )
        self.login_response = client.post(
            reverse('user_view'),
            valid_json,
            format='json'
        )

    def test_get_success_token_retrive(self):
        response = client.get(
            reverse('user_view'),
            {},
            format='json',
            HTTP_jwtToken=self.login_response.json()['token']
        )
        self.assertIn('token', response.json())

    def test_failed_token_retrive(self):
        response = client.get(
            reverse('user_view'),
            {},
            format='json',
            HTTP_jwtToken="kjkopjdw0-9e0r9kjbkfbkwjgeouiew"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
