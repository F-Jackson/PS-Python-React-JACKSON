from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from jwt_auth.serializers import SToken
from jwt_auth.user_auth import verify_user_auth, invalid_token
from payment.contants import FRETE_UNIT_VALUE, FRETE_BONUS_MIN_VALUE
from payment.logic.payment import PaymentHandler
from payment.logic.price_checker import PriceCheckerHandler


class PriceCheckerViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="Get price from user cart",
        operation_description=f"Get the total price of user cart adding a frete price per of {FRETE_UNIT_VALUE}, if "
                              f"total price is equal or greater than {FRETE_BONUS_MIN_VALUE} the frete truns into 0",
        manual_parameters=[
            openapi.Parameter("jwtToken", openapi.IN_HEADER, description="jwt token", type=openapi.TYPE_STRING,
                              required=True),
        ],
        responses={
            200: openapi.Response("Retrives a client Token", SToken)
        }
    )
    def list(self, request) -> Response:
        jwt_is_valid = verify_user_auth(request, True)

        if jwt_is_valid:
            token, user = jwt_is_valid

            data = {
                'token': token
            }

            price_checker = PriceCheckerHandler(data=data, user=user, request_data=request.data)
            price_checker.check()

            data['price'] = price_checker.price

            return Response(data, status=status.HTTP_200_OK)
        return invalid_token()


class PaymentViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="User payment",
        operation_description=f"Pay for the total price of user product-cart",
        manual_parameters=[
            openapi.Parameter("jwtToken", openapi.IN_HEADER, description="jwt token", type=openapi.TYPE_STRING,
                              required=True),
        ],
        responses={
            200: openapi.Response("Retrives a client Token", SToken)
        }
    )
    def create(self, request):
        jwt_is_valid = verify_user_auth(request, True)

        if jwt_is_valid:
            token, user = jwt_is_valid

            data = {
                'token': token
            }

            price_checker = PaymentHandler(data=data, user=user, request_data=request.data)

            return price_checker.pay()
        return invalid_token()
