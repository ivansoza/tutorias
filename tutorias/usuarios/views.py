from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from usuarios.forms import CustomUserCreationFormUsuario
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from .models import CustomUser

# Create your views here.


class CoordinadoresListView(ListView):
    model = CustomUser
    template_name = 'users/coordinadores_list.html'
    context_object_name = 'coordinadores'

    def get_queryset(self):
        coordinadores_group = Group.objects.get(name='Coordinador')
        return CustomUser.objects.filter(groups=coordinadores_group)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'coordinador'
        return context
    
class DocentesListView(ListView):
    model = CustomUser
    template_name = 'users/docentes_list.html'
    context_object_name = 'docentes'

    def get_queryset(self):
        docentes_group = Group.objects.get(name='Docente')
        return CustomUser.objects.filter(groups=docentes_group)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'docente'
        return context

class AlumnosListView(ListView):
    model = CustomUser
    template_name = 'users/alumnos_list.html'
    context_object_name = 'alumnos'

    def get_queryset(self):
        alumnos_group = Group.objects.get(name='Alumno')
        return CustomUser.objects.filter(groups=alumnos_group)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_title'] = 'Lista de Alumnos'
        context['breadcrumb_active_item'] = 'Lista de Alumno'
        context['navbar'] = 'alumno'
        return context
    



class CustomUserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationFormUsuario
    template_name = 'registerUser.html'
    success_url = reverse_lazy('alumnos-list')  # Asegúrate de cambiar 'detalle_familiares' por tu URL de destino.

    def form_valid(self, form):
        user = form.save()
        grupo, created = Group.objects.get_or_create(name='Alumno')
        user.groups.add(grupo)
        messages.success(self.request, "Alumno agregado con éxito.")
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, "Error al agregar el usuario. Por favor, corrija los errores en el formulario.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_title'] = 'Registro de Alumnos'
        context['breadcrumb_active_item'] = 'Registrar Alumno'
        context['navbar'] = 'alumno'
        return context