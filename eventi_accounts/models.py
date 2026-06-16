from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    eta = models.PositiveIntegerField(null=True, blank=True)
    telefono = models.PositiveIntegerField(null=True, blank=True)

