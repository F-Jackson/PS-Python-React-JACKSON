from abc import ABC

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

from jwt_auth.logic.create_login_token import ClientTokenLogin
from user.serializers import UserSerializer


class _UserCreationValidator(ABC):
    def __init__(self, request_data, user: User):
        self.request_data = request_data
        self.user = user

    def _fill_data_with_request_data(self, data: dict) -> None:
        for key, value in self.request_data.items():
            data_have_key = key in data.keys()
            value_is_not_empty = str(value).strip() != ''

            if data_have_key and value_is_not_empty:
                data[key] = str(value)

    def _valid_data_has_empty(self, data: dict) -> None:
        data_is_valid = all(value != '' for value in data.values())

        if not data_is_valid:
            raise ValueError()

    def _check_unique_users(self, data: dict) -> None:
        email_exist = User.objects.filter(email=data['email']).exists()
        username_exist = User.objects.filter(username=data['username']).exists()

        user_exists = any([email_exist, username_exist])

        if user_exists:
            raise PermissionError()

    def _check_xss_attack(self, data: dict) -> None:
        verifys = ('email', 'username')

        for verify in verifys:
            if '<script>' in data[verify].lower() or '</script>' in data[verify].lower():
                raise ValueError()


class _UserAutheticator(ABC):
    def __init__(self, request_data: dict, user: User):
        self.request_data = request_data
        self.user = user

    def _request_data_field(self, field: str, field_type) -> None:
        to_user_request_is_invalid = field not in self.request_data or type(self.request_data[field]) != field_type
        if to_user_request_is_invalid:
            raise ValueError()

    def _autheticate_user(self) -> User:
        self._request_data_field('username', str)
        self._request_data_field('password', str)

        user = authenticate(username=self.request_data['username'], password=str(self.request_data['password']))

        if user is not None:
            return user
        raise PermissionError()

    def _create_and_get_client_token(self) -> str:
        client_token = ClientTokenLogin(self.user.pk)
        token_created = client_token.create_login_tokens()

        if token_created:
            return client_token.client_token
        raise ConnectionError()


class UserHandler(_UserAutheticator, _UserCreationValidator):
    def __init__(self, *, request_data: dict | None = None, user: User | None = None, data: dict | None = None):
        super().__init__(request_data, user)
        self.user = user
        self.data = data

    def _send_error(self, data: dict, error: str, http_status: status) -> Response:
        if error:
            data.update({'error': error})

        return Response(data, status=http_status)

    def info(self) -> Response:
        serializer = UserSerializer(self.user)
        self.data.update({'user': serializer.data})
        return Response(self.data, status.HTTP_200_OK)

    def create(self) -> Response:
        try:
            data = {
                'username': '',
                'email': '',
                'password': '',
            }

            self._fill_data_with_request_data(data)

            self._check_unique_users(data)

            self._valid_data_has_empty(data)

            self._check_xss_attack(data)
        except ValueError as e:
            return self._send_error({}, 'Data is not valid for create a user', status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return self._send_error({}, 'Data is not valid for create a user', status.HTTP_400_BAD_REQUEST)
        else:
            User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])

            return Response(status=status.HTTP_201_CREATED)

    def authenticate(self) -> Response:
        try:
            user = self._autheticate_user()
        except ValueError as e:
            return self._send_error({}, 'Request needs a username and a password', status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return self._send_error({}, 'Invalid user credentials', status.HTTP_401_UNAUTHORIZED)
        else:
            self.user = user
            try:
                client_token = self._create_and_get_client_token()
            except ConnectionError as e:
                return self._send_error({}, 'Error while trying to create jwt tokens',
                                        status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                return Response({'token': client_token}, status=status.HTTP_200_OK)


def invalid_token() -> Response:
    return Response({'error': 'Invalid jwt token'}, status=status.HTTP_401_UNAUTHORIZED)
