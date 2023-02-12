from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

from payment.logic.price_checker import PriceCheckerHandler
from product_cart.models import ProductCart


def _clean_cart_items(user: User):
    cart_items = ProductCart.objects.filter(user=user)

    for cart_item in cart_items:
        cart_item.delete()


class PaymentHandler:
    def __init__(self, *, data: dict, user: User, request_data: dict):
        self._data = data
        self._user = user
        self._request_data = request_data

    def pay(self) -> Response:
        price_checker = PriceCheckerHandler(data=self._data, user=self._user, request_data=self._request_data)
        price_checker.check()
        price = price_checker.price

        _clean_cart_items(self._user)

        return Response(self._data, status=status.HTTP_200_OK)
