from jwt_auth.logic._common import JwtAuthApi
from jwt_auth.models import RefreshTokens


class ClientTokenLogin:
    """
        Jwt Client Token Manager
    """

    def __init__(self, user_id: int):
        self._user_id = user_id
        self._client_token: str | None = None

    def create_login_tokens(self) -> bool:
        """
            Create a Jwt Client Token
        """

        self._delete_refresh_token()

        try:
            self._client_token = JwtAuthApi.create_news_tokens(self._user_id)
        except ValueError:
            self._client_token = None
        else:
            return self._client_token is not None

    @property
    def client_token(self) -> str | None:
        """
            Get Jwt Client Token
        """ 

        return self._client_token

    def _delete_refresh_token(self):
        """
            Detele Jwt Refresh Token From Server
        """ 

        try:
            refresh_token = RefreshTokens.objects.get(user_id=self._user_id)
        except RefreshTokens.DoesNotExist:
            pass
        else:
            refresh_token.delete()
