from django.contrib.auth.models import User

from payment.contants import FRETE_UNIT_VALUE, FRETE_BONUS_MIN_VALUE
from product_cart.models import ProductCart


class PriceCheckerHandler:
    def __init__(self, *, data: dict, user: User, request_data: dict):
        self._data = data
        self._user = user
        self._request_data = request_data
        self._price = 0

    def check(self) -> None:
        price = 0
        frete_price = 0

        items = ProductCart.objects.filter(user=self._user)

        product_prices: list[int] = [getattr(item.product, 'price') for item in items]

        for product_price in product_prices:
            price += product_price
            frete_price += FRETE_UNIT_VALUE

        price_with_frete = price + frete_price
        final_price = price if price_with_frete >= FRETE_BONUS_MIN_VALUE else price_with_frete

        self._price = final_price

    @property
    def price(self) -> float or int:
        return self._price
