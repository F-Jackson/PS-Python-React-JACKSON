from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from games.constants import MEGABYTE_IMAGE_SIZE_LIMIT
from games.models import GamesModel

client = APIClient()


class GamesAddInCartTestCase(APITestCase):
    def setUp(self) -> None:
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
        self.url = reverse('products_cart_view')

    def test_add_game_in_user_cart(self):
        response = client.post(
            self.url,
            {
                'product': self.game_model.pk,
                'qtd': 2
            },
            format='json',
            HTTP_jwtToken=self.token
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_game_in_user_cart_fail_because_of_product_does_not_exist(self):
        response = client.post(
            self.url,
            {
                'product': 102,
                'qtd': 2
            },
            format='json',
            HTTP_jwtToken=self.token
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_game_in_user_cart_fail_because_of_request_attrs_missing(self):
        response = client.post(
            self.url,
            {
                'product': 1
            },
            format='json',
            HTTP_jwtToken=self.token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GamesListInCartTestCase(APITestCase):
    def setUp(self) -> None:
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

        client.post(
            reverse('products_cart_view'),
            {
                'product': self.game_model.pk,
                'qtd': 5
            },
            format='json',
            HTTP_jwtToken=self.token
        )

    def test_if_can_get_products_from_the_cart(self):
        response = client.get(
            reverse('products_cart_view'),
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_token_is_received_from_response(self):
        response = client.get(
            reverse('products_cart_view'),
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        self.assertIn('token', response.json())

    def test_if_games_is_received_from_response(self):
        response = client.get(
            reverse('products_cart_view'),
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        self.assertIn('games', response.json())

    def test_len_games_is_received_from_response_right(self):
        response = client.get(
            reverse('products_cart_view'),
            {},
            format='json',
            HTTP_jwtToken=self.token
        )

        games = response.json()['games']
        self.assertEqual(len(games), 5)


class GamesRemoveInCartTestCase(APITestCase):
    def setUp(self) -> None:
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

        client.post(
            reverse('products_cart_view'),
            {
                'product': self.game_model.pk,
                'qtd': 5
            },
            format='json',
            HTTP_jwtToken=self.token
        )

    def test_remove_in_the_cart(self):
        response = client.delete(
            reverse("products_cart_view"),
            {
                'delete_products': [(self.game_model.pk, 3)]
            },
            format='json',
            HTTP_jwtToken=self.token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_length_before_and_after_remotion(self):
        before_len = len(client.get(
            reverse("products_cart_view"),
            {},
            format='json',
            HTTP_jwtToken=self.token
        ).json()['games'])

        client.delete(
            reverse("products_cart_view"),
            {
                'delete_products': [(self.game_model.pk, 3)]
            },
            format='json',
            HTTP_jwtToken=self.token
        )

        after_len = len(client.get(
            reverse('products_cart_view'),
            {},
            format='json',
            HTTP_jwtToken=self.token
        ).json()['games'])

        self.assertLess(after_len, before_len)

    def test_token_receive(self):
        response = client.delete(
            reverse("products_cart_view"),
            {
                'delete_products': [(self.game_model.pk, 3)]
            },
            format='json',
            HTTP_jwtToken=self.token
        )

        self.assertIn('token', response.json())
