from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from generales.models import Posgrado

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Hombre'),
        ('F', 'Mujer'),
    )
    gender = models.CharField(_('género'), max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    apellido_materno = models.CharField(_('apellido materno'), max_length=150, blank=True, null=True)
    posgrado_alumno = models.ForeignKey(Posgrado, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_("Posgrado Alumno"), related_name='alumnos')
    posgrado_docente = models.ManyToManyField(Posgrado, blank=True, verbose_name=_("Posgrado Docente"), related_name='docentes')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between and includes the apellido_materno if it exists.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        if self.apellido_materno:
            full_name += ' %s' % self.apellido_materno
        return full_name.strip()
    
class TutorAlumno(models.Model):
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tutorados')
    alumno = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tutor_asignado')

    def __str__(self):
        return f'{self.tutor.get_full_name()} tutor de {self.alumno.get_full_name()}'

    class Meta:
        verbose_name = "Tutoría de Alumno"
        verbose_name_plural = "Tutorías de Alumnos"


    class Meta:
        verbose_name = "Tutoría de Alumno"
        verbose_name_plural = "Tutorías de Alumnos"
        unique_together = ('tutor', 'alumno') 

class Coordinador(models.Model):
    posgrado = models.OneToOneField(Posgrado, on_delete=models.CASCADE, verbose_name="Posgrado", related_name='coordinador')
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Usuario Coordinador")

    def __str__(self):
        return f'Coordinador de {self.posgrado.nombre}: {self.usuario.get_full_name()}'


