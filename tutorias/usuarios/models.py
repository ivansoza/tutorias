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
    def __str__(self):
        """
        Returns the full name as the string representation of the user.
        """
        return self.get_full_name()
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

    SEMESTRE_ORDINALES = {
        1: "Primero",
        2: "Segundo",
        3: "Tercero",
        4: "Cuarto",
        5: "Quinto",
        6: "Sexto",
        7: "Séptimo",
        8: "Octavo",
        9: "Noveno",
        10: "Décimo"
    }

    def __str__(self):
        nombre_semestre = self.SEMESTRE_ORDINALES.get(self.numero, f"{self.numero}º")
        return f"{nombre_semestre} "

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
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_finalizacion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Finalización")
    fecha_oficio = models.DateField(verbose_name="Fecha de Anexo", blank=True, null=True)

    class Meta:
        abstract = True

class Anexo1(BaseAnexo):
    domicilio = models.TextField(verbose_name="Domicilio", blank=True, null=True)
    telefono_casa = models.CharField(max_length=15, verbose_name="Teléfono (casa)", blank=True, null=True)
    telefono_celular = models.CharField(max_length=15, verbose_name="Teléfono (celular)", blank=True, null=True)
    correo_electronico1 = models.EmailField(verbose_name="Correo Electrónico 1", blank=True, null=True)
    correo_electronico2 = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico 2")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=100, verbose_name="Lugar de Nacimiento", blank=True, null=True)
    curp = models.CharField(max_length=18, verbose_name="CURP", blank=True, null=True)
    estado_civil = models.CharField(max_length=50, verbose_name="Estado Civil", blank=True, null=True)
    dependientes_economicos = models.IntegerField(verbose_name="Dependientes Económicos", blank=True, null=True)
    licenciatura = models.CharField(max_length=100, verbose_name="Licenciatura", blank=True, null=True)
    institucion_licenciatura = models.CharField(max_length=150, verbose_name="Institución donde cursó la Licenciatura", blank=True, null=True)
    promedio_licenciatura = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Promedio obtenido en la Licenciatura", blank=True, null=True)
    opcion_titulacion = models.CharField(max_length=100, verbose_name="Opción de Titulación", blank=True, null=True)
    nombre_tesis = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre de la Tesis (en su caso)")
    idioma_ingles_toefl = models.IntegerField(verbose_name="Idioma Inglés (TOEFL) %", blank=True, null=True)
    beca_tipo = models.CharField(max_length=100, verbose_name="Beca y Tipo de Beca", blank=True, null=True)
    observaciones_anexo1 = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Anexo 1"
        verbose_name_plural = "Anexos 1"

    def __str__(self):
        return f"Anexo 1 - {self.alumno.get_full_name()} - Semestre {self.semestre.numero}"


class Anexo2(BaseAnexo):
    director_tesis = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='anexo2_director_tesis', verbose_name="Director de Tesis",
        limit_choices_to={'groups__name': 'Docente'}
    )
    codirector_tesis = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='anexo2_codirector_tesis', verbose_name="Codirector de Tesis",
        limit_choices_to={'groups__name': 'Docente'}
    )
    revisor_tesis = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='anexo2_revisor_tesis', verbose_name="Revisor de Tesis",
        limit_choices_to={'groups__name': 'Docente'}
    )
    nombre_tesis = models.CharField(max_length=150, verbose_name="Nombre de la Tesis", blank=True, null=True)
    avance_tesis = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Avance en el Trabajo de Tesis (%)", blank=True, null=True)
    cambio_tema_tesis = models.BooleanField(default=False, verbose_name="¿Ha hecho cambio en el tema de tesis?", blank=True, null=True)
    cambio_director_tesis = models.BooleanField(default=False, verbose_name="¿Ha hecho cambio de director de tesis?", blank=True, null=True)
    cambio_director_detalle = models.TextField(blank=True, null=True, verbose_name="Especificar cambio de director de tesis")
    tesis_registrada_conacyt = models.BooleanField(default=False, verbose_name="¿Tiene su tesis registrada en plataforma CONACYT?", blank=True, null=True)

    # Calificaciones obtenidas hasta la fecha (5 materias como ejemplo)
    # Materia 1
    materia1 = models.CharField(max_length=100, verbose_name="Materia 1", blank=True, null=True)
    calificacion1_materia1 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 1 Materia 1", blank=True, null=True)
    calificacion2_materia1 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 2 Materia 1", blank=True, null=True)
    promedio_materia1 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Promedio Materia 1", blank=True, null=True)

    # Materia 2
    materia2 = models.CharField(max_length=100, verbose_name="Materia 2", blank=True, null=True)
    calificacion1_materia2 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 1 Materia 2", blank=True, null=True)
    calificacion2_materia2 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 2 Materia 2", blank=True, null=True)
    promedio_materia2 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Promedio Materia 2", blank=True, null=True)

    # Materia 3
    materia3 = models.CharField(max_length=100, verbose_name="Materia 3", blank=True, null=True)
    calificacion1_materia3 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 1 Materia 3", blank=True, null=True)
    calificacion2_materia3 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 2 Materia 3", blank=True, null=True)
    promedio_materia3 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Promedio Materia 3", blank=True, null=True)

    # Materia 4
    materia4 = models.CharField(max_length=100, verbose_name="Materia 4", blank=True, null=True)
    calificacion1_materia4 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 1 Materia 4", blank=True, null=True)
    calificacion2_materia4 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 2 Materia 4", blank=True, null=True)
    promedio_materia4 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Promedio Materia 4", blank=True, null=True)

    # Materia 5
    materia5 = models.CharField(max_length=100, verbose_name="Materia 5", blank=True, null=True)
    calificacion1_materia5 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 1 Materia 5", blank=True, null=True)
    calificacion2_materia5 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación 2 Materia 5", blank=True, null=True)
    promedio_materia5 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Promedio Materia 5", blank=True, null=True)

    dificultad_materia = models.TextField(blank=True, null=True, verbose_name="¿Tiene dificultad alta con alguna(s) materia(s)? Mencione cual(es)")
    dificultad_aprendizaje_profesor = models.TextField(blank=True, null=True, verbose_name="¿Considera que la dificultad en el aprendizaje se debe al profesor?")
    conocimientos_previos = models.TextField(blank=True, null=True, verbose_name="¿Considera que no tiene los conocimientos previos para cursar alguna de las materias del programa?")
    observaciones_tutor = models.TextField(blank=True, null=True, verbose_name="Observaciones del tutor sobre el desempeño del estudiante")

    class Meta:
        verbose_name = "Anexo 2"
        verbose_name_plural = "Anexos 2"

    def __str__(self):
        return f"Anexo 2 - {self.alumno.get_full_name()} - Semestre {self.semestre.numero}"


class Anexo3(BaseAnexo):
    director_tesis = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='anexo3_director_tesis', verbose_name="Director de Tesis",
        limit_choices_to={'groups__name': 'Docente'}
    )
    codirector_tesis = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='anexo3_codirector_tesis', verbose_name="Codirector de Tesis",
        limit_choices_to={'groups__name': 'Docente'}
    )
    revisor_tesis = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='anexo3_revisor_tesis', verbose_name="Revisor de Tesis",
        limit_choices_to={'groups__name': 'Docente'}
    )
    nombre_tesis = models.CharField(max_length=150, verbose_name="Nombre de la Tesis", blank=True, null=True)
    avance_tesis = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Avance en el Trabajo de Tesis (%)", blank=True, null=True)

    # Calificaciones obtenidas en el semestre para 5 materias como ejemplo
    # Materia 1
    materia1 = models.CharField(max_length=100, verbose_name="Materia 1", blank=True, null=True)
    calificacion_materia1 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación Materia 1", blank=True, null=True)

    # Materia 2
    materia2 = models.CharField(max_length=100, verbose_name="Materia 2", blank=True, null=True)
    calificacion_materia2 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación Materia 2", blank=True, null=True)

    # Materia 3
    materia3 = models.CharField(max_length=100, verbose_name="Materia 3", blank=True, null=True)
    calificacion_materia3 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación Materia 3", blank=True, null=True)

    # Materia 4
    materia4 = models.CharField(max_length=100, verbose_name="Materia 4", blank=True, null=True)
    calificacion_materia4 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación Materia 4", blank=True, null=True)

    # Materia 5
    materia5 = models.CharField(max_length=100, verbose_name="Materia 5", blank=True, null=True)
    calificacion_materia5 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación Materia 5", blank=True, null=True)

    observaciones_tutor = models.TextField(blank=True, null=True, verbose_name="Observaciones del tutor sobre el desempeño del estudiante")

    class Meta:
        verbose_name = "Anexo 3"
        verbose_name_plural = "Anexos 3"

    def __str__(self):
        return f"Anexo 3 - {self.alumno.get_full_name()} - Semestre {self.semestre.numero}"
