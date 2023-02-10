from django.db import models


class RefreshTokens(models.Model):
    key = models.CharField(max_length=1200, primary_key=True, unique=True)
    user_id = models.IntegerField(unique=True)
    ass = models.IntegerField(default=1)
