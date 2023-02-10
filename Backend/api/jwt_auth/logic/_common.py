from random import randint

import jwt
from django.utils import timezone
from pathlib import os
from dotenv import load_dotenv

from jwt_auth.constants._exp_times import CLIENT_EXP_TIME, REFRESH_EXP_TIME
from jwt_auth.models import RefreshTokens

load_dotenv()

REFRESH_SECRET_KEY = str(os.environ.get('JWT_SECRET_KEY'))
JWT_ALGORITHM = 'HS256'


class JwtAuthApi:
    @classmethod
    def decode_jwt(cls, jwt_key: str, options: dict = None) -> dict:
        return jwt.decode(
            jwt=jwt_key,
            key=REFRESH_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options=options
        )

    @classmethod
    def create_client_token(cls, user_id: int, ass_number: int) -> str:
        client_token = cls._create_token(user_id, CLIENT_EXP_TIME, ass_number)
        return client_token

    @classmethod
    def create_news_tokens(cls, user_id: int) -> str:
        if type(user_id) != int:
            raise ValueError('User id needs to be a integer')

        refresh_token = cls._create_refresh_token(user_id)

        refresh_token_user: int = getattr(refresh_token, 'user_id')
        refresh_token_ass: int = getattr(refresh_token, 'ass')

        return cls.create_client_token(refresh_token_user, refresh_token_ass)

    @classmethod
    def generate_random_ass_refresh_token(cls, refresh_token: RefreshTokens) -> None:
        refresh_token.ass = randint(1, 100000000)
        refresh_token.save()

    @classmethod
    def _create_token(cls, user_id: int, expire_minutes: int, ass: int = None) -> str:
        sub = user_id
        iat = timezone.now()
        exp = timezone.now() + timezone.timedelta(minutes=expire_minutes)

        payload = {
            'sub': sub,
            'iat': iat,
            'exp': exp
        }

        if ass:
            payload['ass'] = ass

        jwt_encoded = jwt.encode(payload=payload, key=REFRESH_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return jwt_encoded

    @classmethod
    def _create_refresh_token(cls, user_id: int) -> RefreshTokens:
        new_token = cls._create_token(user_id, REFRESH_EXP_TIME)
        new_refresh_token = RefreshTokens.objects.create(key=new_token, user_id=user_id)
        new_refresh_token.save()

        cls.generate_random_ass_refresh_token(new_refresh_token)

        return new_refresh_token
