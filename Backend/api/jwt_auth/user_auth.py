from django.contrib.auth.models import User

from jwt_auth.logic.verify_client_token import ClientTokenVerifier
from jwt_auth.serializers import SToken


def verify_user_auth(request, get_user: bool = False) -> None | list[SToken, [User]]:
    """
        Verify jwt auth
        If Jwt is valid return a list[token[user_instance]]
    """

    token = str(request.META.get('HTTP_jwtToken'))
    if token:
        jwt = ClientTokenVerifier(token)
        jwt_is_valid = jwt.valid_client_token()
        if jwt_is_valid:
            token = jwt.client_token[0]
            user_id = jwt.client_token[1]['sub']

            data = [token]

            if get_user:
                try:
                    user = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    return None
                else:
                    data.append(user)

            return data
    return None
