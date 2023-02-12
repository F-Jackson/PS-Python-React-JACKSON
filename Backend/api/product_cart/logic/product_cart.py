from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

from games.models import GamesModel
from games.serializers import GamesSerializer
from product_cart.models import ProductCart


def _delete_items(game: GamesModel, qtd: int):
    items = ProductCart.objects.filter(product=game)

    for item, _ in tuple(zip(items, range(qtd))):
        item.delete()


class RequestVerifier:
    def __init__(self, request_data: dict):
        self.request_data = request_data

    def verify_keys_exists(self, keys: list[str]) -> None:
        for key in keys:
            if key not in self.request_data:
                raise ValueError('Request key erros')

    def verify_keys_types(self, keys_and_type: list[dict[str, type]]) -> None:
        for key_and_type in keys_and_type:
            for key, key_type in key_and_type.items():
                if type(self.request_data[key]) is not key_type:
                    raise ValueError('Request key erros')


class ErrorHandler:
    def __init__(self, error: Exception, status_code: status, data: dict):
        self.error = error
        self.data = data
        self.data['error'] = str(self.error)
        self.status = status_code

    def err(self) -> Response:
        return Response(self.data, status=self.status)


class ProductCartHandler:
    def __init__(self, *, request_data: dict, user: User, data: dict):
        self.request_data = request_data
        self.user = user
        self.data = data

    def create(self) -> Response:
        try:
            request_verifier = RequestVerifier(self.request_data)
            request_verifier.verify_keys_exists(['qtd', 'product'])
            request_verifier.verify_keys_types([{'qtd': int}, {'product': int}])

            game = GamesModel.objects.get(pk=self.request_data['product'])
        except ValueError as e:
            error_handler = ErrorHandler(e, status.HTTP_400_BAD_REQUEST, self.data)
            return error_handler.err()
        except GamesModel.DoesNotExist as e:
            error_handler = ErrorHandler(e, status.HTTP_404_NOT_FOUND, self.data)
            return error_handler.err()
        else:
            for num in range(self.request_data['qtd']):
                ProductCart.objects.create(product=game, user=self.user)
            return Response(self.data, status=status.HTTP_201_CREATED)

    def list_all_products(self) -> Response:
        carts = ProductCart.objects.filter(user=self.user)
        games = GamesSerializer([cart.product for cart in carts], many=True)
        self.data['games'] = games.data
        return Response(self.data, status=status.HTTP_200_OK)

    def remove(self) -> Response:
        try:
            request_verifier = RequestVerifier(self.request_data)

            request_verifier.verify_keys_exists(['delete_products'])
            request_verifier.verify_keys_types([{'delete_products': list}])
        except ValueError as e:
            error_handler = ErrorHandler(e, status.HTTP_400_BAD_REQUEST, self.data)
            return error_handler.err()
        else:
            for product_qtd in self.request_data['delete_products']:
                id, qtd = product_qtd
                if qtd == 0:
                    continue
                try:
                    game = GamesModel.objects.get(pk=id)
                except GamesModel.DoesNotExist as e:
                    continue
                else:
                    _delete_items(game, qtd)

            return Response(self.data, status=status.HTTP_200_OK)

