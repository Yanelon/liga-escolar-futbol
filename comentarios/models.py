from django.db import models


class Comentario(models.Model):
    nombre = models.CharField(
        max_length=80
    )

    comentario = models.TextField(
        max_length=500
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.nombre} - {self.fecha:%d/%m/%Y}"

    class Meta:
        ordering = ["-fecha"]