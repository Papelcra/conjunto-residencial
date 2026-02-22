from django.db import models
from django.conf import settings
from django.utils import timezone

class ZonaComun(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la zona")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    capacidad = models.PositiveIntegerField(default=1, verbose_name="Capacidad máxima")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")

    def __str__(self):
        return self.nombre

class Horario(models.Model):
    zona = models.ForeignKey(ZonaComun, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=20, choices=[
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ])
    hora_inicio = models.TimeField(verbose_name="Hora inicio")
    hora_fin = models.TimeField(verbose_name="Hora fin")

    def __str__(self):
        return f"{self.zona} - {self.dia_semana} {self.hora_inicio}-{self.hora_fin}"

class Reserva(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('cancelada', 'Cancelada'),
    )

    residente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'rol': 'residente'}, verbose_name="Residente")
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, verbose_name="Horario")
    fecha = models.DateField(default=timezone.now, verbose_name="Fecha de reserva")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name="Estado")
    notas = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        unique_together = ('horario', 'fecha')  # No permitir doble reserva en mismo horario/fecha

    def __str__(self):
        return f"Reserva de {self.residente} en {self.horario.zona} para {self.fecha}"