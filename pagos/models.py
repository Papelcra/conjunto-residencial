from django.conf import settings
from django.db import models
from apartamentos.models import Apartamento


class Pago(models.Model):
    ESTADOS_PAGO = (
        ('pendiente', 'Pendiente de verificación'),
        ('aprobado', 'Aprobado / Pagado'),
        ('rechazado', 'Rechazado'),
        ('anulado', 'Anulado'),
    )

    apartamento = models.ForeignKey(
        Apartamento,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name="Apartamento"
    )

    residente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagos_notificados',
        verbose_name="Residente que notificó"
    )

    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Monto pagado"
    )

    fecha_pago = models.DateField(
        verbose_name="Fecha en que se realizó el pago"
    )

    periodo = models.CharField(
        max_length=100,
        verbose_name="Período administrado"
    )

    comprobante = models.FileField(
        upload_to='comprobantes/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Comprobante (imagen o PDF)"
    )

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS_PAGO,
        default='pendiente',
        verbose_name="Estado del pago"
    )

    notas_admin = models.TextField(
        blank=True,
        verbose_name="Comentarios del administrador"
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.periodo} - {self.apartamento} ({self.estado})"


class Notificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.titulo}"