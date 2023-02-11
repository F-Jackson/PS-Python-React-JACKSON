from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserHistoryCallModel(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        unique=False, related_name='from_user',
        related_query_name='from_user'
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        unique=False, related_name='to_user',
        related_query_name='to_user'
    )
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True, blank=True)
    denied = models.BooleanField(default=False)
    already_updated = models.BooleanField(default=False)
