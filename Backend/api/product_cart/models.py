from django.contrib.auth.models import User
from django.db import models

from games.models import GamesModel


class ProductCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(GamesModel, on_delete=models.CASCADE)
