from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class Anuncio(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo