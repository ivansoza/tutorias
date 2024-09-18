from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from generales.models import Posgrado
from .models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm



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