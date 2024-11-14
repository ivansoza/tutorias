from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from generales.models import Posgrado
from .models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm
from django.forms import DateInput


from django.contrib.auth import get_user_model

class CustomUserCreationFormUsuario(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Ordena los campos según deseas que aparezcan en el formulario
        fields = ('username','first_name', 'last_name', 'apellido_materno', 'email', 'password1', 'password2', 'gender', 'posgrado_alumno')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFormUsuario, self).__init__(*args, **kwargs)

        # Configuración del campo 'username' para usar 'Número de Control' como placeholder y label
        self.fields['username'].widget.attrs.update({'placeholder': 'Número de Control'})
        self.fields['username'].label = 'Número de Control'
        self.fields['last_name'].label = 'Apellido Paterno'  # Cambio aquí

        # Configuración de placeholders para otros campos
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Nombre'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Apellido Paterno'})
        self.fields['apellido_materno'].widget.attrs.update({'placeholder': 'Apellido Materno'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Correo Electrónico'})

        # Hacer que los campos sean requeridos según sea necesario
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['apellido_materno'].required = True

        # Campos adicionales
        self.fields['gender'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['gender'].required = False  # Si el género es opcional
        self.fields['gender'].choices = [('', 'Seleccione Género'),] + list(self.fields['gender'].choices)[1:]  # Asegúrate de tener las opciones necesarias


        self.fields['posgrado_alumno'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['posgrado_alumno'].queryset = Posgrado.objects.all()
        self.fields['posgrado_alumno'].label = 'Posgrado'
        self.fields['posgrado_alumno'].required = True

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class CustomUserEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'apellido_materno', 'email', 'gender', 'posgrado_alumno')
    
    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Número de Control', 'readonly': True})  # Assuming username should not be editable
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Nombre'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Apellido Paterno'})
        self.fields['apellido_materno'].widget.attrs.update({'placeholder': 'Apellido Materno'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Correo Electrónico'})
        self.fields['gender'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['gender'].choices = [('', 'Seleccione Género'),] + list(self.fields['gender'].choices)[1:]
        self.fields['posgrado_alumno'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['posgrado_alumno'].queryset = Posgrado.objects.all()
        self.fields.pop('password', None)  # Removing password field if existing in UserChangeForm

class CustomUserCreationFormDocente(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'apellido_materno', 'email', 'password1', 'password2', 'gender', 'posgrado_docente')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFormDocente, self).__init__(*args, **kwargs)

        # Configuración del campo 'username' para usar 'Número de Identificación' como placeholder y label
        self.fields['username'].widget.attrs.update({'placeholder': 'Número de Identificación'})
        self.fields['username'].label = 'Número de Identificación'
        self.fields['last_name'].label = 'Apellido Paterno'

        # Configuración de placeholders para otros campos
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Nombre'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Apellido Paterno'})
        self.fields['apellido_materno'].widget.attrs.update({'placeholder': 'Apellido Materno'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Correo Electrónico'})

        # Ajustes del campo de género
        self.fields['gender'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['gender'].required = False
        self.fields['gender'].choices = [('', 'Seleccione Género'),] + list(self.fields['gender'].choices)[1:]

        # Configuración para el campo de posgrado de docente
        self.fields['posgrado_docente'].widget = forms.SelectMultiple(attrs={'class': 'select2'})
        self.fields['posgrado_docente'].queryset = Posgrado.objects.all()
        self.fields['posgrado_docente'].label = 'Posgrados'
        self.fields['posgrado_docente'].required = True

        # Ajustes para los campos de contraseña
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


        
CustomUser = get_user_model()

class CustomUserEditFormDocente(UserChangeForm):
    password = None  # Esto deshabilita los campos de contraseña en el formulario

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'apellido_materno', 'email', 'gender', 'posgrado_docente')
        widgets = {
            'posgrado_docente': forms.SelectMultiple(attrs={'class': 'select2'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserEditFormDocente, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Número de Identificación', 'readonly': True})
        self.fields['email'].widget.attrs.update({'readonly': True})  # Suponiendo que el correo tampoco debería ser editable

from .models import Anexo1, Anexo2, Anexo3

class Anexo1Form(forms.ModelForm):
    class Meta:
        model = Anexo1
        exclude = ['semestre', 'alumno', 'tutor', 'estado', 'fecha_creacion', 'fecha_finalizacion', 'observaciones']

class Anexo1TutorForm(forms.ModelForm):
    class Meta:
        model = Anexo1
        exclude = ['alumno', 'tutor', 'fecha_creacion', 'fecha_finalizacion','semestre']

    def __init__(self, *args, **kwargs):
        super(Anexo1TutorForm, self).__init__(*args, **kwargs)
        
        # Configuración de placeholders para los campos
        self.fields['domicilio'].widget.attrs.update({
            'rows': 2,
            'placeholder': 'Ingrese el domicilio completo'
        })
        self.fields['telefono_casa'].widget.attrs.update({
            'placeholder': 'Ingrese el teléfono de casa'
        })
        self.fields['telefono_celular'].widget.attrs.update({
            'placeholder': 'Ingrese el teléfono celular'
        })
        self.fields['correo_electronico1'].widget.attrs.update({
            'placeholder': 'Ingrese el primer correo electrónico'
        })
        self.fields['correo_electronico2'].widget.attrs.update({
            'placeholder': 'Ingrese el segundo correo electrónico'
        })
      # Configurar el widget de fecha_nacimiento con formato
        self.fields['fecha_nacimiento'].widget = DateInput(
            attrs={
                'type': 'date',  # HTML5 date input
                'class': 'form-control',  # Agrega clases CSS si es necesario
            },
            format='%Y-%m-%d'
        )
        self.fields['fecha_nacimiento'].input_formats = ['%Y-%m-%d']


        self.fields['fecha_oficio'].widget = DateInput(
            attrs={
                'type': 'date',  # HTML5 date input
                'class': 'form-control',  # Agrega clases CSS si es necesario
            },
            format='%Y-%m-%d'
        )
        self.fields['fecha_oficio'].input_formats = ['%Y-%m-%d']


        self.fields['lugar_nacimiento'].widget.attrs.update({
            'placeholder': 'Ingrese el lugar de nacimiento'
        })
        self.fields['curp'].widget.attrs.update({
            'placeholder': 'Ingrese el CURP'
        })
        self.fields['estado_civil'].widget.attrs.update({
            'placeholder': 'Seleccione el estado civil'
        })
        self.fields['dependientes_economicos'].widget.attrs.update({
            'placeholder': 'Ingrese el número de dependientes económicos'
        })
        self.fields['licenciatura'].widget.attrs.update({
            'placeholder': 'Ingrese la licenciatura'
        })
        self.fields['institucion_licenciatura'].widget.attrs.update({
            'placeholder': 'Ingrese la institución donde cursó la licenciatura'
        })
        self.fields['promedio_licenciatura'].widget.attrs.update({
            'placeholder': 'Ingrese el promedio obtenido'
        })
        self.fields['opcion_titulacion'].widget.attrs.update({
            'placeholder': 'Ingrese la opción de titulación'
        })
        self.fields['nombre_tesis'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la tesis (si aplica)'
        })
        self.fields['idioma_ingles_toefl'].widget.attrs.update({
            'placeholder': 'Ingrese el porcentaje de TOEFL en inglés'
        })
        self.fields['beca_tipo'].widget.attrs.update({
            'placeholder': 'Ingrese el tipo de beca'
        })
        self.fields['observaciones_anexo1'].widget.attrs.update({
            'placeholder': 'Ingrese observaciones adicionales',
            'rows': 2,

        })
        self.fields['estado'].widget.attrs.update({
            'class': 'form-control'
        })
        
        # Configurar el campo observaciones con filas y placeholder
        self.fields['observaciones'].widget.attrs.update({
            'rows': 3,
            'placeholder': 'Observaciones para el alumno'
        })

class Anexo2Form(forms.ModelForm):
    class Meta:
        model = Anexo2
        exclude = ['semestre', 'alumno', 'tutor', 'estado', 'fecha_creacion', 'fecha_finalizacion', 'observaciones']

class Anexo2TutorForm(forms.ModelForm):
    class Meta:
        model = Anexo2
        exclude = ['semestre', 'alumno', 'tutor', 'fecha_creacion', 'fecha_finalizacion']

    def __init__(self, *args, **kwargs):
        super(Anexo2TutorForm, self).__init__(*args, **kwargs)
        
        # Configuración de placeholders y clases para materias y calificaciones
        self.fields['materia1'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 1'
        })
        self.fields['calificacion1_materia1'].widget.attrs.update({
            'placeholder': 'Calificación 1 de Materia 1'
        })
        self.fields['calificacion2_materia1'].widget.attrs.update({
            'placeholder': 'Calificación 2 de Materia 1'
        })
        self.fields['promedio_materia1'].widget.attrs.update({
            'placeholder': 'Promedio de Materia 1'
        })

        self.fields['materia2'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 2'
        })
        self.fields['calificacion1_materia2'].widget.attrs.update({
            'placeholder': 'Calificación 1 de Materia 2'
        })
        self.fields['calificacion2_materia2'].widget.attrs.update({
            'placeholder': 'Calificación 2 de Materia 2'
        })
        self.fields['promedio_materia2'].widget.attrs.update({
            'placeholder': 'Promedio de Materia 2'
        })

        self.fields['materia3'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 3'
        })
        self.fields['calificacion1_materia3'].widget.attrs.update({
            'placeholder': 'Calificación 1 de Materia 3'
        })
        self.fields['calificacion2_materia3'].widget.attrs.update({
            'placeholder': 'Calificación 2 de Materia 3'
        })
        self.fields['promedio_materia3'].widget.attrs.update({
            'placeholder': 'Promedio de Materia 3'
        })

        self.fields['materia4'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 4'
        })
        self.fields['calificacion1_materia4'].widget.attrs.update({
            'placeholder': 'Calificación 1 de Materia 4'
        })
        self.fields['calificacion2_materia4'].widget.attrs.update({
            'placeholder': 'Calificación 2 de Materia 4'
        })
        self.fields['promedio_materia4'].widget.attrs.update({
            'placeholder': 'Promedio de Materia 4'
        })

        self.fields['materia5'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 5'
        })
        self.fields['calificacion1_materia5'].widget.attrs.update({
            'placeholder': 'Calificación 1 de Materia 5'
        })
        self.fields['calificacion2_materia5'].widget.attrs.update({
            'placeholder': 'Calificación 2 de Materia 5'
        })
        self.fields['promedio_materia5'].widget.attrs.update({
            'placeholder': 'Promedio de Materia 5'
        })

        # Configuración previa de campos adicionales (directores y detalles)
        self.fields['director_tesis'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seleccione el Director de Tesis'
        })
        self.fields['codirector_tesis'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seleccione el Codirector de Tesis'
        })
        self.fields['revisor_tesis'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seleccione el Revisor de Tesis'
        })
        self.fields['nombre_tesis'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la tesis',
            'rows': 2
        })
        self.fields['avance_tesis'].widget.attrs.update({
            'placeholder': 'Ingrese el avance en %'
        })
        self.fields['cambio_tema_tesis'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '¿Ha cambiado el tema de tesis?'
        })
        self.fields['cambio_director_tesis'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '¿Ha cambiado el director de tesis?'
        })
        self.fields['cambio_director_detalle'].widget.attrs.update({
            'placeholder': 'Especifique el cambio de director de tesis',
            'rows': 2
        })
        self.fields['tesis_registrada_conacyt'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '¿Está registrada en CONACYT?'
        })
        self.fields['estado'].widget.attrs.update({
            'class': 'form-control'
        })
        
        # Configuración del campo observaciones con filas y placeholder
        self.fields['observaciones'].widget.attrs.update({
            'rows': 3,
            'placeholder': 'Observaciones para el alumno'
        })

        self.fields['dificultad_materia'].widget.attrs.update({
            'placeholder': 'Describe la dificultad en la materia',
            'rows': 2
        })
        self.fields['dificultad_aprendizaje_profesor'].widget.attrs.update({
            'placeholder': 'Describe cualquier dificultad de aprendizaje relacionada con el profesor',
            'rows': 2
        })
        self.fields['conocimientos_previos'].widget.attrs.update({
            'placeholder': 'Describe los conocimientos previos requeridos',
            'rows': 2
        })
        self.fields['observaciones_tutor'].widget.attrs.update({
            'placeholder': 'Observaciones adicionales del tutor',
            'rows': 2
        })

        self.fields['fecha_oficio'].widget = DateInput(
            attrs={
                'type': 'date',  # HTML5 date input
                'class': 'form-control',  # Agrega clases CSS si es necesario
            },
            format='%Y-%m-%d'
        )
        self.fields['fecha_oficio'].input_formats = ['%Y-%m-%d']

class Anexo3Form(forms.ModelForm):
    class Meta:
        model = Anexo3
        exclude = ['semestre', 'alumno', 'tutor', 'estado', 'fecha_creacion', 'fecha_finalizacion', 'observaciones']

class Anexo3TutorForm(forms.ModelForm):
    class Meta:
        model = Anexo3
        exclude = ['semestre', 'alumno', 'tutor', 'fecha_creacion', 'fecha_finalizacion']

    def __init__(self, *args, **kwargs):
        super(Anexo3TutorForm, self).__init__(*args, **kwargs)

        self.fields['director_tesis'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seleccione el Director de Tesis'
        })
        self.fields['codirector_tesis'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seleccione el Codirector de Tesis'
        })
        self.fields['revisor_tesis'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seleccione el Revisor de Tesis'
        })


        self.fields['nombre_tesis'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la tesis',
            'rows': 2
        })
        self.fields['avance_tesis'].widget.attrs.update({
            'placeholder': 'Ingrese el avance en %'
        })

        self.fields['materia1'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 1'
        })

        self.fields['materia2'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 2'
        })

        self.fields['materia3'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 3'
        })

        self.fields['materia4'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 4'
        })

        self.fields['materia5'].widget.attrs.update({
            'placeholder': 'Ingrese el nombre de la Materia 5'
        })

        self.fields['calificacion_materia1'].widget.attrs.update({
            'placeholder': 'Calificación  de Materia 1'
        })
        self.fields['calificacion_materia2'].widget.attrs.update({
            'placeholder': 'Calificación  de Materia 2'
        })
        self.fields['calificacion_materia3'].widget.attrs.update({
            'placeholder': 'Calificación  de Materia 3'
        })
        self.fields['calificacion_materia4'].widget.attrs.update({
            'placeholder': 'Calificación  de Materia 4'
        })

        self.fields['calificacion_materia5'].widget.attrs.update({
            'placeholder': 'Calificación  de Materia 5'
        })

        self.fields['observaciones_tutor'].widget.attrs.update({
            'placeholder': 'Observaciones adicionales del tutor',
            'rows': 2
        })

        self.fields['fecha_oficio'].widget = DateInput(
            attrs={
                'type': 'date',  # HTML5 date input
                'class': 'form-control',  # Agrega clases CSS si es necesario
            },
            format='%Y-%m-%d'
        )
        self.fields['fecha_oficio'].input_formats = ['%Y-%m-%d']
