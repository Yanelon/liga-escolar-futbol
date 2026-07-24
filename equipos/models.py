from django.db import models

# Create your models here.
class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    grupo = models.CharField(max_length=20)
    escudo = models.ImageField(upload_to='escudos/', blank=True, null=True)

    def clean(self):
        self.nombre = self.nombre.strip().title()

        if Equipo.objects.exclude(pk=self.pk).filter(
            nombre__iexact=self.nombre
        ).exists():
            raise ValidationError({
                "nombre": "Ya existe un equipo con ese nombre."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre