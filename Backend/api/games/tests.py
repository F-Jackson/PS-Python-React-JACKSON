from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from games.constants import GAMES_LIST_RECEIVE_LENGTH, MEGABYTE_IMAGE_SIZE_LIMIT
from games.models import GamesModel


class GamesListTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('games_view')
        self.content_type = 'json'

    def test_games_list_length(self):
        response = self.client.get(
            self.url,
            {},
            self.content_type
        )

        response_length = len(response.json())

        self.assertLessEqual(response_length, GAMES_LIST_RECEIVE_LENGTH)


class GameTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = 'game_view'
        self.content_type = 'json'
        self.model = GamesModel.objects.create(name="test", price=120, score=120)

    def test_response_status_200(self):
        response = self.client.get(
            reverse(self.url, [self.model.pk]),
            {},
            self.content_type
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_status_404(self):
        response = self.client.get(
            reverse(self.url, [1001]),
            {},
            self.content_type
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GameImageTestCase(TestCase):
    def setUp(self) -> None:
        one_mb = 1024 * 1024

        fake_fail_image = bytes(one_mb * MEGABYTE_IMAGE_SIZE_LIMIT * 2)
        self.fake_failed_image_size = SimpleUploadedFile("fake.jpg", fake_fail_image, content_type="image/jpeg")

        fake_sucess_image = bytes(one_mb * MEGABYTE_IMAGE_SIZE_LIMIT)
        self.fake_sucess_image_size = SimpleUploadedFile("fake.jpg", fake_sucess_image, content_type="image/jpeg")


    def test_fail_to_upload_image_because_exceded_the_limit_size(self):
        try:
            GamesModel.objects.create(name="test_ok_image", price=120, score=120, image=self.fake_failed_image_size)
        except ValidationError as e:
            self.assertEqual(e, ValidationError(f'Image size must be no more than {MEGABYTE_IMAGE_SIZE_LIMIT} MB'))
        else:
            self.fail('ValidationError not raised')

    def test_sucess_to_upload_image_because_exceded_the_limit_size(self):
        try:
            my_model = GamesModel.objects.create(name="test_ok_image", price=120, score=120,
                                                 image=self.fake_sucess_image_size)
        except ValidationError as e:
            self.fail(str(e))
        else:
            self.assertTrue(GamesModel.objects.filter(pk=my_model.pk).exists())

    def test_fail_to_upload_image_because_of_xss_attack(self):
        try:
            image = self.fake_sucess_image_size
            image.name = '<script>'
            GamesModel.objects.create(name="test_ok_image", price=120, score=120,
                                      image=image)
        except ValidationError as e:
            self.assertEqual(e, ValidationError(f'Xss Attack'))
        else:
            self.fail('ValidationError not raised')


class GameNameTestCase(TestCase):
    def setUp(self) -> None:
        one_mb = 1024 * 1024
        fake_sucess_image = bytes(one_mb * MEGABYTE_IMAGE_SIZE_LIMIT)
        self.fake_sucess_image_size = SimpleUploadedFile("fake.jpg", fake_sucess_image, content_type="image/jpeg")

    def test_fail_to_upload_because_name_of_xss_attack(self):
        try:
            GamesModel.objects.create(name="test_ok<Script>", price=120, score=120,
                                      image=self.fake_sucess_image_size)
        except ValidationError as e:
            self.assertEqual(e, ValidationError(f'Xss Attack'))
        else:
            self.fail('ValidationError not raised')

    def test_sucess_to_upload_because_name_of_xss_attack(self):
        try:
            my_model = GamesModel.objects.create(name="test_ok", price=120, score=120,
                                      image=self.fake_sucess_image_size)
        except ValidationError as e:
            self.fail(e)
        else:
            self.assertTrue(GamesModel.objects.filter(pk=my_model.pk).exists())
