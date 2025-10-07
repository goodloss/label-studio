import uuid

from django.contrib.auth.models import AbstractUser
from users.models import User
from django.db import models


class WKUser(User):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # phone = models.CharField(max_length=16, unique=True, blank=True, null=True)
    # phone_verified = models.BooleanField(default=False)
    pass
