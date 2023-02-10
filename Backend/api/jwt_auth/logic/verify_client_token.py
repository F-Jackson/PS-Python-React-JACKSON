from jwt_auth.logic._common import JwtAuthApi
from jwt_auth.models import RefreshTokens
import jwt


class ClientTokenVerifier:
    """
        Verify Jwt Client Token
    """

    def __init__(self, client_token: str):
        if not isinstance(client_token, str):
            raise ValueError('Client token needs to be a string')

        self._client_token = client_token
        self._refresh_token: RefreshTokens | None = None

    def valid_client_token(self) -> bool:
        """
            Valid Client Token
        """

        try:
            self._first_verify(self._client_token)
        except jwt.exceptions.ExpiredSignatureError:
            self._handle_client_expired_token()
        except:
            self._client_token = None
        finally:
            return self._client_token is not None

    @property
    def client_token(self) -> tuple[str, dict]:
        """
            Get Jwt Client Token
        """

        return self._client_token, JwtAuthApi.decode_jwt(self._client_token)

    def _first_verify(self, token: str):
        """
            First Jwt Client Token Verify
        """

        decode_options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_nbf": True,
            "verify_iat": True,
            "verify_aud": True,
            "verify_iss": True,
            "require": ['sub', 'iat', 'exp'],
        }

        JwtAuthApi.decode_jwt(token, decode_options)

    def _handle_client_expired_token(self) -> None:
        """
            Handle If Client Token is Expired
        """

        try:
            decode_options = {
                "verify_signature": True,
                "verify_exp": False,
                "verify_nbf": True,
                "verify_iat": True,
                "verify_aud": True,
                "verify_iss": True,
                "require": ['sub', 'iat', 'exp', 'ass'],
            }

            payload = JwtAuthApi.decode_jwt(self._client_token, decode_options)
        except:
            self._client_token = None
        else:
            self._get_refresh_token(payload)

            if self._refresh_token:
                self._handle_refresh_token()
            else:
                self._client_token = None

    def _get_refresh_token(self, payload: dict) -> None:
        """
           Get Refresh Token
        """

        user_id = payload['sub']
        ass = payload['ass']

        try:
            refresh_token = RefreshTokens.objects.get(user_id=user_id, ass=ass)
        except RefreshTokens.DoesNotExist:
            pass
        else:
            self._refresh_token = refresh_token

    def _handle_refresh_token(self) -> None:
        """
            Handle Refresh Token
        """

        refresh_token_key: str = getattr(self._refresh_token, 'key')
        refresh_token_user: int = getattr(self._refresh_token, 'user_id')

        try:
            self._first_verify(refresh_token_key)
        except jwt.exceptions.ExpiredSignatureError:
            self._refresh_token.delete()
            self._client_token = JwtAuthApi.create_news_tokens(refresh_token_user)
        except:
            self._client_token = None
        else:
            JwtAuthApi.generate_random_ass_refresh_token(self._refresh_token)

            refresh_token_ass: int = getattr(self._refresh_token, 'ass')

            self._client_token = JwtAuthApi.create_client_token(refresh_token_user, refresh_token_ass)
