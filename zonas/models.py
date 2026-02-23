from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q


class ZonaComun(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Zona común"
        verbose_name_plural = "Zonas comunes"
        ordering = ["nombre"]


class Reserva(models.Model):
    zona = models.ForeignKey(
        'zonas.ZonaComun',
        on_delete=models.CASCADE,
        related_name="reservas"
    )
    residente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas"
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    creada_en = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validar que hora_fin sea mayor que hora_inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser mayor que la hora de inicio.")

        # Validar solapamiento de horarios
        reservas_existentes = Reserva.objects.filter(
            zona=self.zona,
            fecha=self.fecha
        ).filter(
            Q(hora_inicio__lt=self.hora_fin) &
            Q(hora_fin__gt=self.hora_inicio)
        )

        # Excluir la misma reserva si se está editando
        if self.pk:
            reservas_existentes = reservas_existentes.exclude(pk=self.pk)

        if reservas_existentes.exists():
            raise ValidationError("Ya existe una reserva en ese horario.")

    def save(self, *args, **kwargs):
        self.clean()  # Ejecutar validaciones antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.zona} - {self.fecha} ({self.hora_inicio} - {self.hora_fin})"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-fecha", "hora_inicio"]