from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from jwt_auth.serializers import SToken
from jwt_auth.user_auth import verify_user_auth, invalid_token
from product_cart.logic.product_cart import ProductCartHandler


class ProductsCartViewset(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_summary="Get all games in user cart",
        operation_description=f"Get a list that contains all games in user product cart",
        manual_parameters=[
            openapi.Parameter("jwtToken", openapi.IN_HEADER, description="jwt token", type=openapi.TYPE_STRING,
                              required=True),
        ],
        responses={
            200: openapi.Response("Retrives a client Token", SToken)
        }
    )
    def list(self, request):
        jwt_is_valid = verify_user_auth(request, True)

        if jwt_is_valid:
            token, user = jwt_is_valid

            data = {
                'token': token
            }

            product_handler = ProductCartHandler(request_data=request.data, user=user, data=data)

            return product_handler.list_all_products()
        return invalid_token()

    @swagger_auto_schema(
        operation_summary="Add games in user cart",
        operation_description=f"Add games in user product cart given the product and the volume that do user want to "
                              f"in user cart",
        manual_parameters=[
            openapi.Parameter("jwtToken", openapi.IN_HEADER, description="jwt token", type=openapi.TYPE_STRING,
                              required=True),
            openapi.Parameter('product', openapi.IN_QUERY, description='product id', type=openapi.TYPE_NUMBER,
                              required=True),
            openapi.Parameter('qtd', openapi.IN_QUERY, description='volume of games that will add in the user cart',
                              type=openapi.TYPE_NUMBER, required=True),
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

            product_handler = ProductCartHandler(request_data=request.data, user=user, data=data)

            return product_handler.create()
        return invalid_token()

    @swagger_auto_schema(
        operation_summary="Add games in user cart",
        operation_description=f"Add games in user product cart given the product and the volume that do user want to "
                              f"in user cart",
        manual_parameters=[
            openapi.Parameter("jwtToken", openapi.IN_HEADER, description="jwt token", type=openapi.TYPE_STRING,
                              required=True),
            openapi.Parameter('delete_products', openapi.IN_QUERY, description='list of [game_id:number, volume_to_delete:number]',
                              type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT), required=True),
        ],
        responses={
            200: openapi.Response("Retrives a client Token", SToken)
        }
    )
    def destroy(self, request):
        jwt_is_valid = verify_user_auth(request, True)

        if jwt_is_valid:
            token, user = jwt_is_valid

            data = {
                'token': token
            }

            product_handler = ProductCartHandler(request_data=request.data, user=user, data=data)

            return product_handler.remove()
        return invalid_token()
