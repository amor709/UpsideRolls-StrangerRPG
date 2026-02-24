from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username

    @property
    def is_dm(self):
        return self.groups.filter(name='DM').exists()

    @property
    def is_player(self):
        return self.groups.filter(name='PLAYER').exists()