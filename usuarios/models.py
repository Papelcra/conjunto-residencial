from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('seguridad', 'Seguridad'),
        ('residente', 'Residente'),
    )

    rol = models.CharField(
        max_length=40,  # ← aumentado de 20 a 30
        choices=ROLES,
        default='residente',
        verbose_name="Rol del usuario"
    )
    telefono = models.CharField(max_length=30, blank=True, null=True)
    documento = models.CharField(max_length=30, unique=True, blank=True, null=True)

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
    
    @property
    def apartamento(self):
        """
        Devuelve el apartamento donde este usuario es el ocupante_actual.
        Retorna None si no tiene apartamento asignado.
        """
        try:
            return self.apartamentos_ocupados.first()
        except AttributeError:
            return None
    

class RecuperacionSolicitud(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='solicitudes_recuperacion')
    email = models.EmailField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    procesada = models.BooleanField(default=False)
    fecha_procesada = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Solicitud de Recuperación"
        verbose_name_plural = "Solicitudes de Recuperación"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Solicitud de {self.email} - {self.fecha_solicitud.date()}" 