from django.db import models
from django.conf import settings
from apartamentos.models import Apartamento


class Mantenimiento(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('proceso', 'En proceso'),
        ('completado', 'Completado'),
    ]

    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    residente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    respuesta_admin = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.apartamento}"