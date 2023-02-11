from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView

from jwt_auth.serializers import SToken
from jwt_auth.user_auth import verify_user_auth
from user.logic.user import invalid_token, UserHandler
from user.serializers import SUser


class UserView(APIView):
    """
        ViewsetToHandleUser
    """

    @swagger_auto_schema(
        operation_summary="Get User info",
        operation_description="Get User info if authenticated",
        manual_parameters=[
            openapi.Parameter("jwtToken", openapi.IN_HEADER, description="Client Jwt Token",
                              type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: openapi.Response("Retrives new client token and user info", SUser)
        }
    )
    def get(self, request) -> Response(SUser):
        jwt_is_valid = verify_user_auth(request, True)

        if jwt_is_valid:
            token, user = jwt_is_valid

            data = {
                'token': token
            }

            user_handler = UserHandler(user=user, data=data)

            return user_handler.info()
        return invalid_token()


    @swagger_auto_schema(
        operation_summary="Create User",
        operation_description="Create User if User does not exists",
        manual_parameters=[
            openapi.Parameter("username", openapi.IN_QUERY, description="User username", type=openapi.TYPE_STRING,
                              required=True),
            openapi.Parameter("email", openapi.IN_QUERY, description="User email", type=openapi.TYPE_STRING,
                              required=True),
            openapi.Parameter("password", openapi.IN_QUERY, description="User password", type=openapi.TYPE_STRING,
                              required=True)
        ],
        responses={
            201: openapi.Response("Nothing is Retrived")
        }
    )
    def put(self, request) -> Response:
        user_handler = UserHandler(request_data=request.data)
        return user_handler.create()


    @swagger_auto_schema(
        operation_summary="Login User",
        operation_description="Auth User and login, retrives a acess token",
        manual_parameters=[
            openapi.Parameter("username", openapi.IN_QUERY, description="User username", type=openapi.TYPE_STRING,
                              required=True),
            openapi.Parameter("password", openapi.IN_QUERY, description="User password", type=openapi.TYPE_STRING,
                              required=True)
        ],
        responses={
            200: openapi.Response("Retrives a client Token", SToken)
        }
    )
    def post(self, request) -> Response(SToken):
        user_handler = UserHandler(request_data=request.data)
        return user_handler.authenticate()
