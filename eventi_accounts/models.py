from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    eta = models.PositiveIntegerField(null=False, blank=False)
    telefono = models.PositiveIntegerField(null=False, blank=False)

