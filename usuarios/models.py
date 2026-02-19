from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('seguridad', 'Seguridad'),
        ('residente', 'Residente'),
    )

    rol = models.CharField(
        max_length=30,  # ← aumentado de 20 a 30
        choices=ROLES,
        default='residente',
        verbose_name="Rol del usuario"
    )
    telefono = models.CharField(max_length=20, blank=True, null=True)
    documento = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} — {self.get_rol_display()}"

    @property
    def es_admin(self):
        return self.rol == 'admin'

    @property
    def es_seguridad(self):
        return self.rol == 'seguridad'

    @property
    def es_residente(self):
        return self.rol == 'residente'