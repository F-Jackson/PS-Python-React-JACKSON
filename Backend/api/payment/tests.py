from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from games.constants import MEGABYTE_IMAGE_SIZE_LIMIT
from games.models import GamesModel
from payment.contants import FRETE_BONUS_MIN_VALUE

client = APIClient()


class PriceCheckerTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('price_check_view')
        one_mb = 1024 * 1024
        fake_sucess_image_size = bytes(one_mb * MEGABYTE_IMAGE_SIZE_LIMIT)
        fake_sucess_image = SimpleUploadedFile("fake.jpg", fake_sucess_image_size, content_type="image/jpeg")
        self.game_model = GamesModel.objects.create(name="test_ok", price=120, score=120,
                                                    image=fake_sucess_image)
        client.put(
            reverse('user_view'),
            {
                "username": "test",
                "password": "123",
                "email": "test@test.com",
            },
            format='json'
        )
        response = client.post(
            reverse('user_view'),
            {
                "username": "test",
                "password": "123",
                "email": "test@test.com",
            },
            format='json'
        )
        self.token = response.json()['token']

    def test_recive_token(self):
        response = client.get(
            self.url,
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        self.assertIn('token', response.json())

    def test_recive_price(self):
        response = client.get(
            self.url,
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        self.assertIn('price', response.json())

    def test_frete_price_zero(self):
        client.post(
            reverse('products_cart_view'),
            {
                'product': self.game_model.pk,
                'qtd': 2
            },
            format='json',
            HTTP_jwtToken=self.token
        )

        response = client.get(
            self.url,
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        price = response.json()['price']

        self.assertEqual(price, 240)

    def test_frete_price_less_than_bonus_frete(self):
        client.post(
            reverse('products_cart_view'),
            {
                'product': self.game_model.pk,
                'qtd': 1
            },
            format='json',
            HTTP_jwtToken=self.token
        )

        response = client.get(
            self.url,
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        price = response.json()['price']

        self.assertLess(price, FRETE_BONUS_MIN_VALUE)


class PaymentTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('payment_view')
        one_mb = 1024 * 1024
        fake_sucess_image_size = bytes(one_mb * MEGABYTE_IMAGE_SIZE_LIMIT)
        fake_sucess_image = SimpleUploadedFile("fake.jpg", fake_sucess_image_size, content_type="image/jpeg")
        self.game_model = GamesModel.objects.create(name="test_ok", price=120, score=120,
                                                    image=fake_sucess_image)
        client.put(
            reverse('user_view'),
            {
                "username": "test",
                "password": "123",
                "email": "test@test.com",
            },
            format='json'
        )
        response = client.post(
            reverse('user_view'),
            {
                "username": "test",
                "password": "123",
                "email": "test@test.com",
            },
            format='json'
        )
        self.token = response.json()['token']
        self.token = response.json()['token']

        client.post(
            reverse('products_cart_view'),
            {
                'product': self.game_model.pk,
                'qtd': 5
            },
            format='json',
            HTTP_jwtToken=self.token
        )

    def test_payment(self):
        response = client.post(
            self.url,
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_clean_cart(self):
        client.post(
            self.url,
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        response = client.get(
            reverse('products_cart_view'),
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        games = response.json()['games']
        self.assertEqual(len(games), 0)

    def test_token_receive(self):
        response = client.post(
            self.url,
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        self.assertIn('token', response.json())
