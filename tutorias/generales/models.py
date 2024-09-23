from django.db import models

# Create your models here.

class Posgrado(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Posgrado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Posgrado"
        verbose_name_plural = "Posgrados"
        ordering = ['nombre']


