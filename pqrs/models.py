from django.db import models
from usuarios.models import Usuario
import uuid


class PQRS(models.Model):

    TIPO_CHOICES = [
        ('PETICION', 'Petición'),
        ('QUEJA', 'Queja'),
        ('RECLAMO', 'Reclamo'),
        ('SUGERENCIA', 'Sugerencia'),
    ]

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('RESPONDIDO', 'Respondido'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    radicado = models.CharField(max_length=20, unique=True, blank=True)
    respuesta = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')

    def save(self, *args, **kwargs):
        if not self.radicado:
            self.radicado = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.radicado} - {self.usuario.username}"