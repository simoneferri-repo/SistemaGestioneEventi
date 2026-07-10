from django.contrib.auth.models import AbstractUser
from django.db import models

# Personalizzazione del modello AbstractUser per aggiungere i campi eta e telefono
class CustomUser(AbstractUser):
    eta = models.PositiveIntegerField(null=True, blank=True, verbose_name="Età")
    telefono = models.CharField(max_length=20, blank=True, null=True)

