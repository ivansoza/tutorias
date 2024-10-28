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




from django.utils import timezone

class Semestre(models.Model):
    alumno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='semestres')
    numero = models.PositiveIntegerField(verbose_name="Número de Semestre")
    fecha_inicio = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Inicio")
    fecha_fin = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Fin")
    iniciado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"Semestre {self.numero} - {self.alumno.get_full_name()}"

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        ordering = ['numero']
        unique_together = ('alumno', 'numero')


class EstadoAnexo(models.TextChoices):
    EN_PROCESO = 'EN_PROCESO', 'En proceso'
    FINALIZADO = 'FINALIZADO', 'Finalizado'
    REVISADO = 'REVISADO', 'Revisado'

class BaseAnexo(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='%(class)s')
    alumno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_alumno')
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_tutor')
    estado = models.CharField(max_length=20, choices=EstadoAnexo.choices, default=EstadoAnexo.EN_PROCESO)
    observaciones = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='anexos/%Y/%m/%d/', blank=True, null=True)

    # Preguntas de ejemplo
    pregunta1 = models.CharField(max_length=255, blank=True, null=True)
    pregunta2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

class Anexo1(BaseAnexo):
    class Meta:
        verbose_name = "Anexo 1"
        verbose_name_plural = "Anexos 1"

    def __str__(self):
        return f"Anexo 1 - {self.alumno.get_full_name()} - Semestre {self.semestre.numero}"

class Anexo2(BaseAnexo):
    class Meta:
        verbose_name = "Anexo 2"
        verbose_name_plural = "Anexos 2"

    def __str__(self):
        return f"Anexo 2 - {self.alumno.get_full_name()} - Semestre {self.semestre.numero}"

class Anexo3(BaseAnexo):
    class Meta:
        verbose_name = "Anexo 3"
        verbose_name_plural = "Anexos 3"

    def __str__(self):
        return f"Anexo 3 - {self.alumno.get_full_name()} - Semestre {self.semestre.numero}"